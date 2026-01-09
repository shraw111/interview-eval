"use client";

import { Progress } from "@/components/ui/progress";
import { Card, CardContent } from "@/components/ui/card";
import { AgentStates } from "@/lib/websocket/useEvaluationStream";
import { Badge } from "@/components/ui/badge";
import { Zap, Brain, Scale, Target } from "lucide-react";

interface ProgressTrackerProps {
  progress: number;
  agentStates: AgentStates;
  isConnected: boolean;
}

const agents = [
  {
    key: "primary_evaluator" as const,
    name: "Primary Evaluator",
    icon: Brain,
    description: "Initial assessment",
    color: "from-primary to-primary/80",
    position: { x: 20, y: 50 },
  },
  {
    key: "challenge_agent" as const,
    name: "Challenge Agent",
    icon: Scale,
    description: "Critical review",
    color: "from-secondary to-secondary/80",
    position: { x: 50, y: 20 },
  },
  {
    key: "decision_agent" as const,
    name: "Decision Agent",
    icon: Target,
    description: "Final calibration",
    color: "from-success to-success/80",
    position: { x: 80, y: 50 },
  },
];

const getStatusColor = (status: string) => {
  switch (status) {
    case "completed":
      return "text-success border-success/50 bg-success/10";
    case "in_progress":
      return "text-primary border-primary/50 bg-primary/10 pulse-glow";
    case "waiting":
      return "text-muted-foreground border-muted bg-muted/20";
    default:
      return "text-muted-foreground border-muted bg-muted/20";
  }
};

const getStatusIcon = (status: string) => {
  switch (status) {
    case "completed":
      return "✓";
    case "in_progress":
      return <Zap className="w-4 h-4 animate-pulse" />;
    default:
      return "○";
  }
};

export function ProgressTracker({
  progress,
  agentStates,
  isConnected,
}: ProgressTrackerProps) {
  return (
    <div className="space-y-8">
      {/* Connection Status Banner */}
      {!isConnected && (
        <Card className="border-warning/50 bg-warning/5">
          <CardContent className="pt-6 pb-6">
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 rounded-full bg-warning animate-pulse"></div>
              <p className="text-sm text-warning">
                Reconnecting to evaluation stream...
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Neural Network Visualization */}
      <Card className="border-border/50 backdrop-blur-xl bg-card/50 overflow-hidden">
        <CardContent className="pt-8 pb-8">
          {/* Progress Bar */}
          <div className="mb-8">
            <div className="flex justify-between items-center mb-3">
              <span className="text-sm font-semibold">Overall Progress</span>
              <span className="text-2xl font-bold gradient-text">{progress}%</span>
            </div>
            <Progress value={progress} className="h-3" />
            <p className="text-xs text-muted-foreground mt-2">
              {progress === 0 && "Initializing neural evaluation system..."}
              {progress > 0 && progress < 33 && "Primary evaluator analyzing transcript..."}
              {progress >= 33 && progress < 67 && "Challenge agent reviewing assessment..."}
              {progress >= 67 && progress < 100 && "Decision agent calibrating final judgment..."}
              {progress === 100 && "✓ Evaluation complete!"}
            </p>
          </div>

          {/* Neural Network Graph */}
          <div className="relative h-64 mb-8">
            {/* SVG connections between agents */}
            <svg
              className="absolute inset-0 w-full h-full"
              style={{ zIndex: 0 }}
            >
              {/* Connection 1 → 2 */}
              <line
                x1="20%"
                y1="50%"
                x2="50%"
                y2="20%"
                stroke="url(#gradient1)"
                strokeWidth="2"
                strokeDasharray={agentStates.primary_evaluator === "completed" ? "0" : "5,5"}
                className={agentStates.primary_evaluator === "completed" ? "opacity-100" : "opacity-30"}
              />
              {/* Connection 2 → 3 */}
              <line
                x1="50%"
                y1="20%"
                x2="80%"
                y2="50%"
                stroke="url(#gradient2)"
                strokeWidth="2"
                strokeDasharray={agentStates.challenge_agent === "completed" ? "0" : "5,5"}
                className={agentStates.challenge_agent === "completed" ? "opacity-100" : "opacity-30"}
              />
              {/* Gradient definitions */}
              <defs>
                <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="hsl(var(--primary))" />
                  <stop offset="100%" stopColor="hsl(var(--secondary))" />
                </linearGradient>
                <linearGradient id="gradient2" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="hsl(var(--secondary))" />
                  <stop offset="100%" stopColor="hsl(var(--success))" />
                </linearGradient>
              </defs>
            </svg>

            {/* Agent nodes */}
            {agents.map((agent) => {
              const status = agentStates[agent.key];
              const Icon = agent.icon;

              return (
                <div
                  key={agent.key}
                  className="absolute transform -translate-x-1/2 -translate-y-1/2"
                  style={{
                    left: `${agent.position.x}%`,
                    top: `${agent.position.y}%`,
                    zIndex: 10,
                  }}
                >
                  <div className="flex flex-col items-center">
                    {/* Agent Circle */}
                    <div
                      className={`
                        relative w-20 h-20 rounded-full border-2 flex items-center justify-center
                        transition-all duration-500 backdrop-blur-xl
                        ${getStatusColor(status)}
                      `}
                    >
                      {/* Background gradient */}
                      <div className={`absolute inset-0 rounded-full bg-gradient-to-br ${agent.color} opacity-20`}></div>

                      {/* Icon */}
                      <Icon className="w-8 h-8 relative z-10" />

                      {/* Status indicator */}
                      <div className="absolute -top-1 -right-1 w-6 h-6 rounded-full bg-background border-2 border-border flex items-center justify-center text-xs">
                        {getStatusIcon(status)}
                      </div>

                      {/* Pulse rings for active state */}
                      {status === "in_progress" && (
                        <>
                          <div className="absolute inset-0 rounded-full border-2 border-primary animate-ping opacity-75"></div>
                          <div className="absolute inset-0 rounded-full border-2 border-primary animate-ping opacity-50" style={{ animationDelay: "0.5s" }}></div>
                        </>
                      )}
                    </div>

                    {/* Agent Label */}
                    <div className="mt-3 text-center">
                      <p className="text-xs font-semibold whitespace-nowrap">{agent.name}</p>
                      <p className="text-xs text-muted-foreground whitespace-nowrap">{agent.description}</p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Agent Status Cards */}
          <div className="grid grid-cols-3 gap-4">
            {agents.map((agent) => {
              const status = agentStates[agent.key];
              return (
                <Card
                  key={agent.key}
                  className={`border transition-all duration-300 ${
                    status === "in_progress"
                      ? "border-primary/50 bg-primary/5"
                      : status === "completed"
                      ? "border-success/50 bg-success/5"
                      : "border-border/30 bg-muted/20"
                  }`}
                >
                  <CardContent className="pt-4 pb-4">
                    <div className="flex items-center gap-2 mb-1">
                      <div className={`w-2 h-2 rounded-full ${
                        status === "completed"
                          ? "bg-success"
                          : status === "in_progress"
                          ? "bg-primary animate-pulse"
                          : "bg-muted-foreground"
                      }`}></div>
                      <Badge
                        variant="outline"
                        className="text-xs"
                      >
                        {status === "completed" ? "Complete" : status === "in_progress" ? "Processing" : "Waiting"}
                      </Badge>
                    </div>
                    <p className="text-xs font-medium">{agent.name}</p>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Info Card */}
      {progress < 100 && (
        <Card className="border-primary/30 bg-primary/5 backdrop-blur-xl">
          <CardContent className="pt-6 pb-6">
            <div className="flex items-start gap-3">
              <Zap className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-semibold text-primary mb-1">
                  Neural Processing Active
                </p>
                <p className="text-xs text-muted-foreground">
                  Our multi-agent system is collaboratively analyzing the candidate.
                  This typically takes 2-3 minutes. You can safely keep this tab open.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
