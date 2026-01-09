"use client";

import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { UseFormReturn } from "react-hook-form";
import { EvaluationFormData } from "@/lib/validation/schemas";
import { useState } from "react";
import { RUBRIC_TEMPLATES, RubricTemplateKey } from "@/lib/rubric-templates";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface RubricEditorProps {
  form: UseFormReturn<EvaluationFormData>;
}

export function RubricEditor({ form }: RubricEditorProps) {
  const {
    register,
    watch,
    setValue,
    formState: { errors },
  } = form;

  const [selectedTemplate, setSelectedTemplate] = useState<RubricTemplateKey>("standard");
  const rubric = watch("rubric") || "";
  const charCount = rubric.length;

  const handleTemplateChange = (value: RubricTemplateKey) => {
    setSelectedTemplate(value);
    setValue("rubric", RUBRIC_TEMPLATES[value].content, { shouldValidate: true });
  };

  return (
    <div className="space-y-4">
      {/* Helper text */}
      <div className="rounded-lg bg-muted/50 p-3 border border-border">
        <p className="text-sm text-muted-foreground">
          Standard evaluation framework loaded. Select a different template or customize the criteria below to match your specific needs.
        </p>
      </div>

      {/* Template selector */}
      <div className="space-y-2">
        <Label htmlFor="template">Evaluation Template</Label>
        <Select value={selectedTemplate} onValueChange={handleTemplateChange}>
          <SelectTrigger id="template">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {Object.entries(RUBRIC_TEMPLATES).map(([key, template]) => (
              <SelectItem key={key} value={key}>
                {template.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Rubric editor */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <Label htmlFor="rubric">Evaluation Criteria *</Label>
          <span className="text-sm text-muted-foreground">
            {charCount.toLocaleString()} characters
          </span>
        </div>
        <Textarea
          id="rubric"
          rows={20}
          className="font-mono text-sm"
          {...register("rubric")}
        />
        {errors.rubric && (
          <p className="text-sm text-red-500">{errors.rubric.message}</p>
        )}
        {charCount < 50 && charCount > 0 && (
          <p className="text-sm text-amber-600">
            Rubric needs at least {50 - charCount} more characters
          </p>
        )}
      </div>
    </div>
  );
}
