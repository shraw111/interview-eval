"use client";

import { useEffect, useState } from "react";
import { Progress } from "@/components/ui/progress";
import { Card } from "@/components/ui/card";
import { AgentStates } from "@/lib/websocket/useEvaluationStream";
import { Loader2, CheckCircle2, Clock } from "lucide-react";

interface ProgressTrackerProps {
  progress: number;
  agentStates: AgentStates;
  isConnected: boolean;
}

// Map agent states to user-friendly status messages
function getCurrentStatus(
  progress: number,
  agentStates: AgentStates,
  elapsedSeconds: number
): string {
  // Check actual agent states for more accurate status
  if (agentStates.decision_agent.status === "processing") {
    return "Finalizing recommendation";
  }
  if (agentStates.decision_agent.status === "completed") {
    return "Evaluation complete";
  }
  if (agentStates.challenge_agent.status === "processing") {
    return "Reviewing evaluation quality";
  }
  if (agentStates.challenge_agent.status === "completed") {
    return "Preparing final decision";
  }
  if (agentStates.primary_evaluator.status === "processing") {
    return "Analyzing transcript";
  }
  if (agentStates.primary_evaluator.status === "completed") {
    return "Conducting quality review";
  }

  // Use progress for better status if no agent state updates yet
  if (progress === 100) return "Evaluation complete";
  if (progress >= 67) return "Finalizing recommendation";
  if (progress >= 33) return "Reviewing evaluation quality";
  if (progress > 0) return "Analyzing transcript";

  // After 5 seconds, assume it's analyzing even if no progress yet
  if (elapsedSeconds >= 5) return "Analyzing transcript";

  return "Starting evaluation";
}

function formatElapsedTime(seconds: number): string {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  if (mins === 0) return `${secs}s`;
  return `${mins}m ${secs}s`;
}

export function ProgressTracker({
  progress,
  agentStates,
  isConnected,
}: ProgressTrackerProps) {
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const [startTime] = useState(Date.now());

  // Update elapsed time every second
  useEffect(() => {
    const interval = setInterval(() => {
      const elapsed = Math.floor((Date.now() - startTime) / 1000);
      setElapsedSeconds(elapsed);
    }, 1000);

    return () => clearInterval(interval);
  }, [startTime]);

  const currentStatus = getCurrentStatus(progress, agentStates, elapsedSeconds);
  const isComplete = progress === 100;

  return (
    <div className="w-full max-w-2xl mx-auto">
      <Card className="shadow-card border-2">
        <div className="p-12">
          {/* Status Icon & Message */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-4">
              {isComplete ? (
                <CheckCircle2 className="w-8 h-8 text-primary" />
              ) : (
                <Loader2 className="w-8 h-8 text-primary animate-spin" />
              )}
            </div>

            <h2 className="text-2xl font-semibold mb-2">
              {currentStatus}
            </h2>

            <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
              <Clock className="w-4 h-4" />
              <span>
                {isComplete
                  ? `Completed in ${formatElapsedTime(elapsedSeconds)}`
                  : `${formatElapsedTime(elapsedSeconds)} elapsed`
                }
              </span>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="space-y-3 mb-6">
            <div className="flex justify-between items-center text-sm">
              <span className="text-muted-foreground font-medium">Progress</span>
              <span className="text-lg font-semibold text-primary">{progress}%</span>
            </div>
            <Progress value={progress} className="h-3" />
          </div>

          {/* Time Estimate */}
          {!isComplete && (
            <div className="text-center pt-4 border-t border-border/50">
              <p className="text-sm text-muted-foreground">
                Evaluations typically take 3-5 minutes
              </p>
              {!isConnected && (
                <p className="text-xs text-amber-600 mt-2">
                  Reconnecting to server...
                </p>
              )}
            </div>
          )}

          {/* Completion Message */}
          {isComplete && (
            <div className="text-center pt-4 border-t border-border/50">
              <p className="text-sm text-muted-foreground">
                Results are ready below
              </p>
            </div>
          )}
        </div>
      </Card>

      {/* Visual Progress Steps (Optional - subtle) */}
      {!isComplete && (
        <div className="mt-6 flex justify-center gap-2">
          <div className={`h-1.5 w-16 rounded-full transition-all duration-500 ${
            progress >= 33 ? 'bg-primary' : 'bg-border'
          }`} />
          <div className={`h-1.5 w-16 rounded-full transition-all duration-500 ${
            progress >= 66 ? 'bg-primary' : 'bg-border'
          }`} />
          <div className={`h-1.5 w-16 rounded-full transition-all duration-500 ${
            progress >= 100 ? 'bg-primary' : 'bg-border'
          }`} />
        </div>
      )}
    </div>
  );
}
