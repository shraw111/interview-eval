// WebSocket event types

import { AgentNode, EvaluationResult } from "./evaluation";

export interface BaseWebSocketEvent {
  type: string;
  timestamp: string;
}

export interface ConnectedEvent extends BaseWebSocketEvent {
  type: "connected";
  evaluation_id: string;
}

export interface EvaluationStartedEvent extends BaseWebSocketEvent {
  type: "evaluation_started";
  evaluation_id: string;
}

export interface NodeStartedEvent extends BaseWebSocketEvent {
  type: "node_started";
  node: AgentNode;
  progress_percentage: number;
}

export interface NodeCompletedEvent extends BaseWebSocketEvent {
  type: "node_completed";
  node: AgentNode;
  progress_percentage: number;
  output_preview?: string;
  tokens?: {
    input: number;
    output: number;
  };
}

export interface EvaluationCompletedEvent extends BaseWebSocketEvent {
  type: "evaluation_completed";
  evaluation_id: string;
  result: EvaluationResult;
}

export interface ErrorEvent extends BaseWebSocketEvent {
  type: "error";
  error: string;
  node?: AgentNode;
}

export interface HeartbeatEvent extends BaseWebSocketEvent {
  type: "heartbeat";
}

export type WebSocketEvent =
  | ConnectedEvent
  | EvaluationStartedEvent
  | NodeStartedEvent
  | NodeCompletedEvent
  | EvaluationCompletedEvent
  | ErrorEvent
  | HeartbeatEvent;
