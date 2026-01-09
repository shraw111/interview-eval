"use client";

import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { evaluationFormSchema, EvaluationFormData } from "@/lib/validation/schemas";
import { DEFAULT_RUBRIC } from "@/lib/rubric-templates";
import { FormWizard } from "@/components/evaluation/FormWizard";
import { ProgressTracker } from "@/components/evaluation/ProgressTrackerClean";
import { EvaluationResults } from "@/components/evaluation/EvaluationResultsNew";
import { useEvaluationStream } from "@/lib/websocket/useEvaluationStream";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { AlertCircle, RefreshCw, Sparkles, Loader2 } from "lucide-react";

type FlowState = "form" | "processing" | "results" | "error";

export default function HomePage() {
  const [flowState, setFlowState] = useState<FlowState>("form");
  const [evaluationId, setEvaluationId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isResetting, setIsResetting] = useState(false);

  const form = useForm<EvaluationFormData>({
    resolver: zodResolver(evaluationFormSchema),
    defaultValues: {
      candidate_info: {
        name: "",
        current_level: undefined,
        target_level: undefined,
        years_experience: undefined,
        level_expectations: undefined,
      },
      rubric: DEFAULT_RUBRIC,
      transcript: "",
    },
  });

  // Only connect to websocket when we have an evaluation ID
  const { isConnected, progress, agentStates, result, error: streamError } =
    useEvaluationStream(evaluationId || "", { enabled: !!evaluationId });

  // Handle submission
  const handleSubmit = async (data: EvaluationFormData) => {
    setIsSubmitting(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/api/v1/evaluations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to create evaluation");
      }

      const result = await response.json();
      setEvaluationId(result.evaluation_id);
      setFlowState("processing");
    } catch (err: any) {
      setError(err.message || "Failed to start evaluation");
      setFlowState("error");
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle when results are ready - use useEffect to avoid state update during render
  useEffect(() => {
    if (result && flowState === "processing" && evaluationId) {
      // Only transition if we have a valid evaluationId (not showing old results)
      setFlowState("results");
    }
  }, [result, flowState, evaluationId]);

  // Handle stream errors - use useEffect to avoid state update during render
  useEffect(() => {
    if (streamError && flowState === "processing") {
      setError(streamError);
      setFlowState("error");
    }
  }, [streamError, flowState]);

  // Reset to start new evaluation
  const handleReset = () => {
    setIsResetting(true);
    // Add small delay for visual feedback
    setTimeout(() => {
      setFlowState("form");
      setEvaluationId(null);
      setError(null);
      form.reset();
      setIsResetting(false);
    }, 300);
  };

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Hero Header - Always visible */}
        <div className="text-center mb-12 fade-in">
          <h1 className="text-4xl md:text-5xl font-semibold mb-4">
            Interview Evaluation
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            AI-powered evaluation system for candidate assessments
          </p>
        </div>

        {/* State: Form */}
        {flowState === "form" && (
          <div className="scale-in">
            <FormWizard
              form={form}
              onSubmit={handleSubmit}
              isSubmitting={isSubmitting}
            />
          </div>
        )}

        {/* State: Processing */}
        {flowState === "processing" && (
          <div className="fade-in">
            <div className="max-w-4xl mx-auto">
              {/* Candidate Info Header */}
              <div className="text-center mb-12">
                <h2 className="text-3xl font-bold mb-2">
                  {form.getValues("candidate_info.name")}
                </h2>
                <p className="text-lg text-muted-foreground">
                  {form.getValues("candidate_info.current_level")} → {form.getValues("candidate_info.target_level")}
                </p>
              </div>

              {/* Progress Tracker */}
              <ProgressTracker
                progress={progress}
                agentStates={agentStates}
                isConnected={isConnected}
              />
            </div>
          </div>
        )}

        {/* State: Results */}
        {flowState === "results" && result && (
          <div className="fade-in">
            <EvaluationResults result={result} />

            {/* New Evaluation Button */}
            <div className="flex justify-center mt-8">
              <Button
                onClick={handleReset}
                disabled={isResetting}
                size="lg"
                className="gap-2"
              >
                {isResetting ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Resetting...
                  </>
                ) : (
                  <>
                    <RefreshCw className="w-4 h-4" />
                    New Evaluation
                  </>
                )}
              </Button>
            </div>
          </div>
        )}

        {/* State: Error */}
        {flowState === "error" && (
          <div className="max-w-2xl mx-auto fade-in">
            <Card className="border-destructive/50 bg-destructive/5">
              <CardContent className="pt-6">
                <div className="flex items-start gap-4">
                  <AlertCircle className="w-6 h-6 text-destructive shrink-0 mt-1" />
                  <div className="flex-1">
                    <h2 className="text-lg font-semibold text-destructive mb-2">
                      Evaluation Error
                    </h2>
                    <p className="text-sm text-muted-foreground mb-4">
                      {error}
                    </p>
                    <Button
                      onClick={handleReset}
                      disabled={isResetting}
                      variant="outline"
                      className="gap-2"
                    >
                      {isResetting ? (
                        <>
                          <Loader2 className="w-4 h-4 animate-spin" />
                          Resetting...
                        </>
                      ) : (
                        <>
                          <RefreshCw className="w-4 h-4" />
                          Try Again
                        </>
                      )}
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

      </div>
    </div>
  );
}
