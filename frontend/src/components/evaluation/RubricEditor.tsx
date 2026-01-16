"use client";

import { Label } from "@/components/ui/label";
import { UseFormReturn } from "react-hook-form";
import { EvaluationFormData } from "@/lib/validation/schemas";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { CheckCircle2 } from "lucide-react";

interface RubricEditorProps {
  form: UseFormReturn<EvaluationFormData>;
}

const RUBRIC_CRITERIA = [
  { category: "Overall Presentation", weight: "10%", description: "Verbal delivery, pacing, command, and stakeholder engagement" },
  { category: "Presentation Structure", weight: "10%", description: "Logical flow, strategic continuity, and framework usage" },
  { category: "Storytelling Skills", weight: "20%", description: "Narrative flow, business context, and persuasive impact" },
  { category: "Case Study Analysis", weight: "60%", description: "Problem definition, opportunity sizing, research depth, business analysis, GTM strategy, and implementation planning (10 sub-criteria)" },
  { category: "Prototype Creation", weight: "0%", description: "Prototype structure, user flow, and functional connectivity" },
];

export function RubricEditor({ form }: RubricEditorProps) {
  return (
    <div className="space-y-6">
      {/* Helper text */}
      <div className="rounded-lg bg-muted/50 p-3 border border-border">
        <p className="text-sm text-muted-foreground">
          The evaluation framework is standardized and non-editable to ensure consistent assessments across all candidates.
        </p>
      </div>

      {/* Template selector (read-only with only 1 option) */}
      <div className="space-y-2">
        <Label htmlFor="template">Evaluation Framework</Label>
        <Select value="case-study" disabled>
          <SelectTrigger id="template">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="case-study">
              Case Study Presentation Evaluation
            </SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Rubric Summary Card */}
      <Card className="border-2">
        <CardContent className="pt-6">
          <div className="flex items-center gap-2 mb-4">
            <CheckCircle2 className="w-5 h-5 text-primary" />
            <h3 className="font-semibold">Evaluation Criteria Overview</h3>
          </div>

          <div className="space-y-4">
            {RUBRIC_CRITERIA.map((criterion, index) => (
              <div key={index} className="flex items-start gap-3 pb-4 last:pb-0 border-b last:border-0">
                <Badge variant="outline" className="mt-0.5 shrink-0">
                  {criterion.weight}
                </Badge>
                <div className="flex-1">
                  <div className="font-medium text-sm mb-1">
                    {criterion.category}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {criterion.description}
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6 pt-6 border-t">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Scoring Scale:</span>
              <span className="font-medium">1-5 (where 3 = Current Level, 4 = Target Level)</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
