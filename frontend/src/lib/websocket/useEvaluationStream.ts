"use client";

import { useEffect, useState, useCallback, useRef } from "react";
import { WebSocketEvent, NodeCompletedEvent } from "@/types/websocket";
import { AgentNode, EvaluationResult } from "@/types/evaluation";

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";

export interface AgentState {
  status: "pending" | "processing" | "completed";
  tokens?: {
    input: number;
    output: number;
  };
  outputPreview?: string;
}

export interface AgentStates {
  primary_evaluator: AgentState;
  challenge_agent: AgentState;
  decision_agent: AgentState;
}

interface UseEvaluationStreamOptions {
  enabled?: boolean; // Whether to actually connect (default: true)
  onProgress?: (event: WebSocketEvent) => void;
  onComplete?: (result: EvaluationResult) => void;
  onError?: (error: string) => void;
}

export function useEvaluationStream(
  evaluationId: string,
  options: UseEvaluationStreamOptions = {}
) {
  const [isConnected, setIsConnected] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentNode, setCurrentNode] = useState<AgentNode | null>(null);
  const [agentStates, setAgentStates] = useState<AgentStates>({
    primary_evaluator: { status: "pending" },
    challenge_agent: { status: "pending" },
    decision_agent: { status: "pending" },
  });
  const [result, setResult] = useState<EvaluationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectAttempts = useRef(0);
  const maxReconnectAttempts = 5;
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  // Refs to avoid stale closures
  const resultRef = useRef<EvaluationResult | null>(null);
  const isClosingRef = useRef(false);
  const optionsRef = useRef(options);

  // Keep refs in sync with state
  useEffect(() => {
    resultRef.current = result;
  }, [result]);

  useEffect(() => {
    optionsRef.current = options;
  }, [options]);

  // Fallback: Poll REST API if WebSocket fails
  const pollEvaluationStatus = useCallback(async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/evaluations/${evaluationId}`);
      if (response.ok) {
        const data = await response.json();

        // Update progress
        if (data.progress_percentage !== undefined) {
          setProgress(data.progress_percentage);
        }

        // Check if completed
        if (data.status === "completed" && data.result) {
          setResult(data.result);
          // Stop polling
          if (pollIntervalRef.current) {
            clearInterval(pollIntervalRef.current);
            pollIntervalRef.current = null;
          }
        } else if (data.status === "failed") {
          setError(data.error || "Evaluation failed");
          if (pollIntervalRef.current) {
            clearInterval(pollIntervalRef.current);
            pollIntervalRef.current = null;
          }
        }
      }
    } catch (err) {
      console.error("Error polling evaluation status:", err);
    }
  }, [evaluationId]);

  const startPolling = useCallback(() => {
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
    }
    console.log("Starting fallback polling (WebSocket unavailable)");
    pollIntervalRef.current = setInterval(pollEvaluationStatus, 5000);
  }, [pollEvaluationStatus]);

  const connect = useCallback(() => {
    // Prevent connecting if already connected or intentionally closing
    if (wsRef.current?.readyState === WebSocket.OPEN || isClosingRef.current) {
      return;
    }

    const wsUrl = `${WS_URL}/ws/evaluations/${evaluationId}`;
    console.log("Connecting to WebSocket:", wsUrl);

    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log("WebSocket connected");
      setIsConnected(true);
      setError(null);
      reconnectAttempts.current = 0;
    };

    ws.onmessage = (event) => {
      try {
        const data: WebSocketEvent = JSON.parse(event.data);
        console.log("WebSocket message:", data);

        // Call optional progress callback using ref
        optionsRef.current.onProgress?.(data);

        // Update progress
        if ("progress_percentage" in data && typeof data.progress_percentage === "number") {
          setProgress(data.progress_percentage);
        }

        // Update current node
        if ("node" in data && data.node) {
          setCurrentNode(data.node as AgentNode);
        }

        // Handle different event types
        switch (data.type) {
          case "connected":
            console.log("WebSocket connection confirmed");
            break;

          case "heartbeat":
            // Connection is alive, no action needed
            break;

          case "node_started":
            if (data.node) {
              setAgentStates((prev) => ({
                ...prev,
                [data.node!]: {
                  status: "processing",
                },
              }));
            }
            break;

          case "node_completed":
            if (data.node) {
              const nodeData = data as NodeCompletedEvent;
              setAgentStates((prev) => ({
                ...prev,
                [data.node!]: {
                  status: "completed",
                  tokens: nodeData.tokens,
                  outputPreview: nodeData.output_preview,
                },
              }));
            }
            break;

          case "evaluation_completed":
            if ("result" in data && data.result) {
              setResult(data.result);
              optionsRef.current.onComplete?.(data.result);
            }
            break;

          case "error":
            if ("error" in data && data.error) {
              const errorMsg = data.error as string;
              setError(errorMsg);
              optionsRef.current.onError?.(errorMsg);
            }
            break;
        }
      } catch (err) {
        console.error("Error parsing WebSocket message:", err);
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      // Don't immediately show error - let reconnection handle it
    };

    ws.onclose = () => {
      console.log("WebSocket closed");
      setIsConnected(false);

      // Auto-reconnect with exponential backoff using ref to check result
      if (reconnectAttempts.current < maxReconnectAttempts && !resultRef.current && !isClosingRef.current) {
        const delay = Math.min(1000 * Math.pow(2, reconnectAttempts.current), 10000);
        reconnectAttempts.current++;
        console.log(`Reconnecting in ${delay}ms (attempt ${reconnectAttempts.current})`);
        setTimeout(connect, delay);
      } else if (reconnectAttempts.current >= maxReconnectAttempts && !resultRef.current && !isClosingRef.current) {
        // WebSocket failed - fall back to polling
        console.log("WebSocket reconnection failed, falling back to polling");
        startPolling();
      }
    };

    wsRef.current = ws;
  }, [evaluationId, startPolling]); // Only evaluationId and startPolling as deps

  // Effect to clear state when evaluationId changes or disabled
  useEffect(() => {
    const enabled = options.enabled !== undefined ? options.enabled : true;

    // Clear all state when disabled or evaluationId is empty
    if (!enabled || !evaluationId) {
      setIsConnected(false);
      setProgress(0);
      setCurrentNode(null);
      setAgentStates({
        primary_evaluator: { status: "pending" },
        challenge_agent: { status: "pending" },
        decision_agent: { status: "pending" },
      });
      setResult(null);
      setError(null);
      return;
    }
  }, [evaluationId, options.enabled]);

  // Effect to manage connection lifecycle
  useEffect(() => {
    const enabled = options.enabled !== undefined ? options.enabled : true;

    // Only connect if enabled and we have a valid evaluation ID
    if (!enabled || !evaluationId) {
      return;
    }

    isClosingRef.current = false;
    connect();

    return () => {
      // Mark as intentionally closing to prevent reconnection
      isClosingRef.current = true;
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
    };
  }, [evaluationId, connect, options.enabled]);

  // Separate effect to close connection when result is received
  useEffect(() => {
    if (result && wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      console.log("Evaluation completed, closing WebSocket");
      wsRef.current.close();
    }
  }, [result]);

  return {
    isConnected,
    progress,
    currentNode,
    agentStates,
    result,
    error,
    reconnect: connect,
  };
}
