"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { MarkdownRenderer } from "@/components/shared/MarkdownRenderer";
import { Lightbulb, TrendingUp, Target } from "lucide-react";

interface DetailedFeedbackProps {
  decision: string;
  developmentPlan?: string[];
}

export function DetailedFeedback({ decision, developmentPlan }: DetailedFeedbackProps) {
  // Clean decision text - remove any JSON remnants
  const cleanDecision = (text: string): string => {
    if (!text) return "";

    // Remove lines that look like JSON structure
    const lines = text.split('\n');
    const cleanedLines = lines.filter(line => {
      const trimmed = line.trim();
      // Skip JSON-like lines
      return !(
        trimmed.startsWith('{') ||
        trimmed.startsWith('}') ||
        trimmed.startsWith('"Criterion"') ||
        trimmed.startsWith('"Primary Score"') ||
        trimmed.startsWith('"Challenger Suggested"') ||
        trimmed.startsWith('"Final"') ||
        trimmed.startsWith('"Reason"') ||
        trimmed.startsWith('"decision"') ||
        trimmed.startsWith('"comparison_rows"') ||
        /^\s*[\{\}\[\]]\s*$/.test(trimmed)
      );
    });

    return cleanedLines.join('\n').trim();
  };

  const cleanedDecision = cleanDecision(decision);

  console.log("[DetailedFeedback] Original decision length:", decision?.length);
  console.log("[DetailedFeedback] Cleaned decision length:", cleanedDecision?.length);

  return (
    <div className="space-y-6">
      {/* Main Feedback Card */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-primary" />
            <CardTitle>Detailed Feedback for Candidate</CardTitle>
          </div>
          <p className="text-sm text-muted-foreground mt-2">
            Comprehensive evaluation with strengths, development areas, and actionable recommendations
          </p>
        </CardHeader>
        <CardContent>
          <div className="prose prose-sm max-w-none">
            <MarkdownRenderer content={cleanedDecision} />
          </div>
        </CardContent>
      </Card>

      {/* Development Plan Card (if available from decision_json) */}
      {developmentPlan && developmentPlan.length > 0 && (
        <Card className="border-primary/20 bg-primary/5">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Target className="w-5 h-5 text-primary" />
              <CardTitle className="text-lg">Key Development Actions</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3">
              {developmentPlan.map((item, index) => (
                <li key={index} className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center text-xs font-semibold text-primary mt-0.5">
                    {index + 1}
                  </div>
                  <p className="text-sm leading-relaxed flex-1">{item}</p>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
