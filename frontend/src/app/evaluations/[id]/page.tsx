"use client";

import { useEffect } from "react";
import { useParams } from "next/navigation";
import { useEvaluationStream } from "@/lib/websocket/useEvaluationStream";
import { ProgressTracker } from "@/components/evaluation/ProgressTracker";
import { EvaluationResults } from "@/components/evaluation/EvaluationResults";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { AlertCircle, Loader2, Home } from "lucide-react";
import Link from "next/link";

export default function EvaluationPage() {
  const params = useParams();
  const evaluationId = params.id as string;

  const { isConnected, progress, agentStates, result, error } =
    useEvaluationStream(evaluationId);

  useEffect(() => {
    // Log for debugging
    console.log("Evaluation Page:", {
      evaluationId,
      isConnected,
      progress,
      hasResult: !!result,
      error,
    });
  }, [evaluationId, isConnected, progress, result, error]);

  // Error state
  if (error) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <Card className="border-red-200 bg-red-50">
          <CardContent className="pt-6">
            <div className="flex items-start gap-4">
              <AlertCircle className="w-6 h-6 text-red-600 shrink-0 mt-1" />
              <div className="flex-1">
                <h2 className="text-lg font-semibold text-red-900 mb-2">
                  Evaluation Error
                </h2>
                <p className="text-sm text-red-800 mb-4">{error}</p>
                <Link href="/">
                  <Button variant="outline" className="gap-2">
                    <Home className="w-4 h-4" />
                    Back to Home
                  </Button>
                </Link>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Loading/Progress state
  if (!result) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-slate-900 mb-2">
            Evaluation in Progress
          </h1>
          <p className="text-muted-foreground">
            ID: <span className="font-mono text-sm">{evaluationId}</span>
          </p>
        </div>

        <ProgressTracker
          progress={progress}
          agentStates={agentStates}
          isConnected={isConnected}
        />

        {/* Initial loading state */}
        {progress === 0 && (
          <Card className="mt-6">
            <CardContent className="pt-6">
              <div className="flex items-center gap-3 justify-center py-8">
                <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
                <p className="text-muted-foreground">
                  Initializing evaluation...
                </p>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    );
  }

  // Results state
  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">
          Evaluation Complete
        </h1>
        <p className="text-sm text-muted-foreground">
          Completed in {Math.round(result.metadata.execution_time_seconds)} seconds
        </p>
      </div>

      <EvaluationResults result={result} />
    </div>
  );
}
