"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ComparisonRow } from "@/types/evaluation";
import { ArrowUp, ArrowDown, Minus } from "lucide-react";

interface ScoreComparisonTableProps {
  rows: ComparisonRow[];
}

export function ScoreComparisonTable({ rows }: ScoreComparisonTableProps) {
  // Debug logging
  console.log("[ScoreComparisonTable] Rendering with rows:", rows);
  console.log("[ScoreComparisonTable] Row count:", rows?.length);

  const getScoreChange = (primary: number, final: number) => {
    if (final > primary) return "increase";
    if (final < primary) return "decrease";
    return "same";
  };

  const getChangeIcon = (change: string) => {
    if (change === "increase") return <ArrowUp className="w-4 h-4 text-green-600" />;
    if (change === "decrease") return <ArrowDown className="w-4 h-4 text-red-600" />;
    return <Minus className="w-4 h-4 text-gray-400" />;
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Score Comparison & Final Decisions</CardTitle>
        <p className="text-sm text-muted-foreground">
          Primary evaluator scores vs. challenger suggestions vs. final arbitrator decisions
        </p>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b-2 border-border">
                <th className="text-left py-3 px-4 font-semibold text-sm">Criterion</th>
                <th className="text-center py-3 px-2 font-semibold text-sm">Primary</th>
                <th className="text-center py-3 px-2 font-semibold text-sm">Challenger</th>
                <th className="text-center py-3 px-2 font-semibold text-sm">Final</th>
                <th className="text-center py-3 px-2 font-semibold text-sm">Change</th>
                <th className="text-left py-3 px-4 font-semibold text-sm">Reason</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row, index) => {
                const change = getScoreChange(row["Primary Score"], row.Final);
                return (
                  <tr
                    key={index}
                    className="border-b border-border hover:bg-muted/50 transition-colors"
                  >
                    <td className="py-3 px-4 text-sm font-medium">
                      {row.Criterion}
                    </td>
                    <td className="text-center py-3 px-2">
                      <Badge variant="outline" className="font-mono">
                        {row["Primary Score"]}
                      </Badge>
                    </td>
                    <td className="text-center py-3 px-2">
                      <Badge variant="outline" className="font-mono">
                        {row["Challenger Suggested"]}
                      </Badge>
                    </td>
                    <td className="text-center py-3 px-2">
                      <Badge
                        variant={change === "increase" ? "default" : change === "decrease" ? "destructive" : "secondary"}
                        className="font-mono"
                      >
                        {row.Final}
                      </Badge>
                    </td>
                    <td className="text-center py-3 px-2">
                      {getChangeIcon(change)}
                    </td>
                    <td className="py-3 px-4 text-sm text-muted-foreground">
                      {row.Reason}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}
