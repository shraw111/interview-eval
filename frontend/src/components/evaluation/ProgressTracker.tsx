"use client";

import { Progress } from "@/components/ui/progress";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AgentStatusCard } from "./AgentStatusCard";
import { AgentStates } from "@/lib/websocket/useEvaluationStream";
import { Badge } from "@/components/ui/badge";
import { Wifi, WifiOff } from "lucide-react";

interface ProgressTrackerProps {
  progress: number;
  agentStates: AgentStates;
  isConnected: boolean;
}

export function ProgressTracker({
  progress,
  agentStates,
  isConnected,
}: ProgressTrackerProps) {
  return (
    <div className="space-y-6">
      {/* Connection Status */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="text-lg">Evaluation Progress</CardTitle>
            <Badge variant={isConnected ? "success" : "destructive"} className="gap-1">
              {isConnected ? (
                <>
                  <Wifi className="w-3 h-3" />
                  Connected
                </>
              ) : (
                <>
                  <WifiOff className="w-3 h-3" />
                  Disconnected
                </>
              )}
            </Badge>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Overall Progress</span>
              <span className="font-semibold">{progress}%</span>
            </div>
            <Progress value={progress} className="h-3" />
            <p className="text-xs text-muted-foreground">
              {progress === 0 && "Starting evaluation..."}
              {progress > 0 && progress < 33 && "Primary evaluator analyzing transcript..."}
              {progress >= 33 && progress < 67 && "Challenge agent reviewing evaluation..."}
              {progress >= 67 && progress < 100 && "Decision agent calibrating and deciding..."}
              {progress === 100 && "Evaluation complete!"}
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Agent Status Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <AgentStatusCard
          name="Primary Evaluator"
          icon="🔍"
          state={agentStates.primary_evaluator}
        />
        <AgentStatusCard
          name="Challenge Agent"
          icon="⚔️"
          state={agentStates.challenge_agent}
        />
        <AgentStatusCard
          name="Decision Agent"
          icon="🎯"
          state={agentStates.decision_agent}
        />
      </div>

      {/* Instructions */}
      {progress < 100 && (
        <Card className="bg-blue-50 border-blue-200">
          <CardContent className="pt-6">
            <p className="text-sm text-blue-900">
              <strong>Please keep this tab open.</strong> The evaluation typically takes 2-3
              minutes. You&apos;ll see real-time updates as each agent completes their analysis.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
