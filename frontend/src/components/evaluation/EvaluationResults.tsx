"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { EvaluationResult } from "@/types/evaluation";
import { EvaluationJourney } from "./EvaluationJourney";
import { Download, Home, TrendingUp, Clock, DollarSign, Cpu } from "lucide-react";
import Link from "next/link";

interface EvaluationResultsProps {
  result: EvaluationResult;
}

export function EvaluationResults({ result }: EvaluationResultsProps) {
  const { candidate_info, decision, metadata } = result;

  const totalTokens = metadata.tokens.total_input + metadata.tokens.total_output;

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="border-2">
        <CardHeader>
          <div className="flex items-start justify-between">
            <div>
              <CardTitle className="text-3xl mb-2">{candidate_info.name}</CardTitle>
              <p className="text-muted-foreground">
                {candidate_info.current_level} → {candidate_info.target_level}
              </p>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                <Clock className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">
                  {Math.round(metadata.execution_time_seconds)}s
                </div>
                <div className="text-xs text-muted-foreground">Execution Time</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-purple-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">
                  {totalTokens.toLocaleString()}
                </div>
                <div className="text-xs text-muted-foreground">Total Tokens</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
                <DollarSign className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">
                  ${metadata.cost_usd.toFixed(2)}
                </div>
                <div className="text-xs text-muted-foreground">Cost (USD)</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-amber-100 flex items-center justify-center">
                <Cpu className="w-5 h-5 text-amber-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">{metadata.model_version}</div>
                <div className="text-xs text-muted-foreground">Model</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Evaluation Journey */}
      <EvaluationJourney result={result} />

      {/* Actions */}
      <div className="flex gap-4 justify-center">
        <Link href="/">
          <Button variant="outline" className="gap-2">
            <Home className="w-4 h-4" />
            New Evaluation
          </Button>
        </Link>
        <Button variant="outline" className="gap-2" disabled>
          <Download className="w-4 h-4" />
          Download Report
        </Button>
      </div>
    </div>
  );
}
