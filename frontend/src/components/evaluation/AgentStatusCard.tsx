"use client";

import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CheckCircle2, Circle, Loader2 } from "lucide-react";
import { AgentState } from "@/lib/websocket/useEvaluationStream";

interface AgentStatusCardProps {
  name: string;
  icon?: string;
  state: AgentState;
}

export function AgentStatusCard({ name, icon, state }: AgentStatusCardProps) {
  const { status, tokens, outputPreview } = state;

  const getStatusIcon = () => {
    switch (status) {
      case "completed":
        return <CheckCircle2 className="w-5 h-5 text-green-500" />;
      case "processing":
        return <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />;
      default:
        return <Circle className="w-5 h-5 text-gray-300" />;
    }
  };

  const getStatusBadge = () => {
    switch (status) {
      case "completed":
        return <Badge variant="success">Completed</Badge>;
      case "processing":
        return <Badge className="bg-blue-500">Processing...</Badge>;
      default:
        return <Badge variant="outline">Pending</Badge>;
    }
  };

  return (
    <Card className={status === "processing" ? "border-blue-500 shadow-lg" : ""}>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            {getStatusIcon()}
            <h3 className="font-semibold text-sm">{name}</h3>
          </div>
          {getStatusBadge()}
        </div>
      </CardHeader>
      <CardContent>
        {tokens && (
          <div className="text-xs text-muted-foreground">
            <div className="flex justify-between">
              <span>Tokens:</span>
              <span className="font-mono">
                {(tokens.input + tokens.output).toLocaleString()}
              </span>
            </div>
            <div className="flex justify-between mt-1">
              <span className="ml-2">Input:</span>
              <span className="font-mono">{tokens.input.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span className="ml-2">Output:</span>
              <span className="font-mono">{tokens.output.toLocaleString()}</span>
            </div>
          </div>
        )}
        {status === "processing" && (
          <div className="mt-2 text-xs text-blue-600 animate-pulse">
            Analyzing...
          </div>
        )}
      </CardContent>
    </Card>
  );
}
