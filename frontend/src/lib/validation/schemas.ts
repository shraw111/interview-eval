import { z } from "zod";

export const candidateInfoSchema = z.object({
  name: z.string().min(1, "Name is required"),
  current_level: z.string().optional(),
  target_level: z.string().optional(),
  years_experience: z
    .number()
    .min(0, "Years of experience must be 0 or greater")
    .max(50, "Years of experience must be 50 or less")
    .optional(),
  level_expectations: z.string().optional(),
});

export const evaluationFormSchema = z.object({
  candidate_info: candidateInfoSchema,
  rubric: z
    .string()
    .min(50, "Rubric must be at least 50 characters")
    .max(50000, "Rubric is too long (max 50,000 characters)"),
  transcript: z
    .string()
    .min(100, "Transcript must be at least 100 characters")
    .max(200000, "Transcript is too long (max 200,000 characters)"),
});

export type EvaluationFormData = z.infer<typeof evaluationFormSchema>;
export type CandidateInfoFormData = z.infer<typeof candidateInfoSchema>;
