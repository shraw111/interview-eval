"use client";

import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { UseFormReturn } from "react-hook-form";
import { EvaluationFormData } from "@/lib/validation/schemas";

interface CandidateInfoFormProps {
  form: UseFormReturn<EvaluationFormData>;
}

export function CandidateInfoForm({ form }: CandidateInfoFormProps) {
  const {
    register,
    formState: { errors },
  } = form;

  return (
    <div className="space-y-4">
      <div>
        <Label htmlFor="name">Candidate Name *</Label>
        <Input
          id="name"
          placeholder="e.g., Sarah Chen"
          {...register("candidate_info.name")}
        />
        {errors.candidate_info?.name && (
          <p className="text-sm text-red-500 mt-1">
            {errors.candidate_info.name.message}
          </p>
        )}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="current_level">
            Current Level <span className="text-muted-foreground text-sm">(optional)</span>
          </Label>
          <Input
            id="current_level"
            placeholder="e.g., L5 PM"
            {...register("candidate_info.current_level")}
          />
          {errors.candidate_info?.current_level && (
            <p className="text-sm text-red-500 mt-1">
              {errors.candidate_info.current_level.message}
            </p>
          )}
        </div>

        <div>
          <Label htmlFor="target_level">
            Target Level <span className="text-muted-foreground text-sm">(optional)</span>
          </Label>
          <Input
            id="target_level"
            placeholder="e.g., L6 Senior PM"
            {...register("candidate_info.target_level")}
          />
          {errors.candidate_info?.target_level && (
            <p className="text-sm text-red-500 mt-1">
              {errors.candidate_info.target_level.message}
            </p>
          )}
        </div>
      </div>

      <div>
        <Label htmlFor="years_experience">
          Years at Current Level <span className="text-muted-foreground text-sm">(optional)</span>
        </Label>
        <Input
          id="years_experience"
          type="number"
          min="0"
          max="50"
          placeholder="0"
          {...register("candidate_info.years_experience", {
            valueAsNumber: true,
            setValueAs: (v) => v === "" ? undefined : Number(v),
          })}
        />
        {errors.candidate_info?.years_experience && (
          <p className="text-sm text-red-500 mt-1">
            {errors.candidate_info.years_experience.message}
          </p>
        )}
      </div>
    </div>
  );
}
