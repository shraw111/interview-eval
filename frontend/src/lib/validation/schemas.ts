import { z } from "zod";

// Helper to convert empty strings to undefined
const optionalString = z.preprocess(
  (val) => (val === "" ? undefined : val),
  z.string().optional()
);

export const candidateInfoSchema = z.object({
  name: z.string().min(1, "Name is required"),
  current_level: optionalString,
  target_level: optionalString,
  years_experience: z.preprocess(
    (val) => {
      // Handle empty string, null, undefined, or NaN
      if (val === "" || val === null || val === undefined || (typeof val === "number" && isNaN(val))) {
        return undefined;
      }
      return Number(val);
    },
    z.number().min(0, "Years of experience must be 0 or greater").max(50, "Years of experience must be 50 or less").optional()
  ),
  level_expectations: optionalString,
});

export const evaluationFormSchema = z.object({
  candidate_info: candidateInfoSchema,
  transcript: z
    .string()
    .min(100, "Transcript must be at least 100 characters")
    .max(200000, "Transcript is too long (max 200,000 characters)"),
});

export type EvaluationFormData = z.infer<typeof evaluationFormSchema>;
export type CandidateInfoFormData = z.infer<typeof candidateInfoSchema>;
