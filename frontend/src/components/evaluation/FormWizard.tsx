"use client";

import { useState, useCallback } from "react";
import { UseFormReturn } from "react-hook-form";
import { EvaluationFormData } from "@/lib/validation/schemas";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { CandidateInfoForm } from "./CandidateInfoForm";
import { RubricEditor } from "./RubricEditor";
import { TranscriptUpload } from "./TranscriptUpload";
import { ChevronRight, ChevronLeft, Play, Loader2 } from "lucide-react";

interface FormWizardProps {
  form: UseFormReturn<EvaluationFormData>;
  onSubmit: (data: EvaluationFormData) => void;
  isSubmitting: boolean;
}

const steps = [
  {
    id: 1,
    title: "Candidate Details",
    subtitle: "Basic information about the candidate and evaluation context",
  },
  {
    id: 2,
    title: "Evaluation Criteria",
    subtitle: "Review and customize the evaluation framework",
  },
  {
    id: 3,
    title: "Interview Content",
    subtitle: "Upload or paste the conversation transcript",
  },
];

export function FormWizard({ form, onSubmit, isSubmitting }: FormWizardProps) {
  const [currentStep, setCurrentStep] = useState(1);
  const [isValidating, setIsValidating] = useState(false);
  const [isNavigating, setIsNavigating] = useState(false);

  const validateStep = useCallback(async (step: number): Promise<boolean> => {
    let fieldsToValidate: any[] = [];

    switch (step) {
      case 1:
        // Only validate required fields (name is the only required field)
        fieldsToValidate = [
          "candidate_info.name",
        ];
        break;
      case 2:
        // Rubric is hardcoded, no validation needed - just allow progression
        return true;
      case 3:
        fieldsToValidate = ["transcript"];
        break;
    }

    const result = await form.trigger(fieldsToValidate as any);
    return result;
  }, [form]);

  const handleNext = useCallback(async () => {
    setIsValidating(true);
    try {
      const isValid = await validateStep(currentStep);
      if (isValid) {
        setCurrentStep((prev) => Math.min(prev + 1, 3));
      }
    } finally {
      setIsValidating(false);
    }
  }, [currentStep, validateStep]);

  const handlePrevious = useCallback(() => {
    setIsNavigating(true);
    // Add small delay for visual feedback
    setTimeout(() => {
      setCurrentStep((prev) => Math.max(prev - 1, 1));
      setIsNavigating(false);
    }, 150);
  }, []);

  const handleSubmit = useCallback(async () => {
    console.log("Start Evaluation clicked - validating form...");
    const isValid = await form.trigger();

    if (!isValid) {
      // Validation failed - get errors
      const errors = form.formState.errors;
      console.error("Form validation failed:", errors);

      // Show which fields are invalid
      Object.keys(errors).forEach(field => {
        console.error(`Field '${field}' error:`, errors[field as keyof typeof errors]);
      });

      return; // Don't submit if invalid
    }

    console.log("Form valid - submitting...");
    onSubmit(form.getValues());
  }, [form, onSubmit]);

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Step Progress Header */}
      <div className="mb-12 fade-in">
        <div className="relative mb-8">
          {/* Connector Lines Container */}
          <div className="absolute top-7 left-0 right-0 flex items-center px-16">
            <div className="flex-1 flex items-center gap-4">
              {/* Line 1-2 */}
              <div
                className={`
                  h-1 flex-1 transition-all duration-300 rounded-full
                  ${currentStep > 1 ? "bg-primary/60" : "bg-border"}
                `}
              />
              {/* Line 2-3 */}
              <div
                className={`
                  h-1 flex-1 transition-all duration-300 rounded-full
                  ${currentStep > 2 ? "bg-primary/60" : "bg-border"}
                `}
              />
            </div>
          </div>

          {/* Steps Container */}
          <div className="relative flex justify-between items-start px-8">
            {steps.map((step) => (
              <div key={step.id} className="flex flex-col items-center">
                {/* Step Circle */}
                <div
                  className={`
                    relative w-14 h-14 rounded-full flex items-center justify-center
                    transition-all duration-300 z-10
                    ${
                      currentStep === step.id
                        ? "bg-primary text-white"
                        : currentStep > step.id
                        ? "bg-primary/80 text-white"
                        : "bg-muted text-muted-foreground"
                    }
                  `}
                >
                  {currentStep > step.id ? (
                    <span className="text-xl font-semibold">✓</span>
                  ) : (
                    <span className="text-xl font-semibold">{step.id}</span>
                  )}
                </div>

                {/* Step Label */}
                <div className="mt-3 text-center">
                  <div
                    className={`
                      text-sm font-semibold transition-colors duration-300 whitespace-nowrap
                      ${
                        currentStep === step.id
                          ? "text-primary"
                          : currentStep > step.id
                          ? "text-primary"
                          : "text-muted-foreground"
                      }
                    `}
                  >
                    {step.title}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Current Step Title */}
        <div className="text-center fade-in-delay-1">
          <h2 className="text-3xl font-semibold mb-2">
            {steps[currentStep - 1].title}
          </h2>
          <p className="text-muted-foreground">
            {steps[currentStep - 1].subtitle}
          </p>
        </div>
      </div>

      {/* Form Content */}
      <Card className="shadow-card fade-in-delay-2">
        <div className="p-8">
          {/* Step 1: Candidate Info */}
          {currentStep === 1 && (
            <div className="space-y-6 slide-up">
              <CandidateInfoForm form={form} />
            </div>
          )}

          {/* Step 2: Rubric */}
          {currentStep === 2 && (
            <div className="space-y-6 slide-up">
              <RubricEditor form={form} />
            </div>
          )}

          {/* Step 3: Transcript */}
          {currentStep === 3 && (
            <div className="space-y-6 slide-up">
              <TranscriptUpload form={form} />
            </div>
          )}
        </div>

        {/* Navigation Footer */}
        <div className="border-t border-border/50 p-6 bg-muted/20">
          <div className="flex items-center justify-between">
            {/* Previous Button */}
            <Button
              type="button"
              variant="ghost"
              onClick={handlePrevious}
              disabled={currentStep === 1 || isNavigating}
              className="gap-2"
            >
              {isNavigating ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Previous
                </>
              ) : (
                <>
                  <ChevronLeft className="w-4 h-4" />
                  Previous
                </>
              )}
            </Button>

            {/* Step Indicator */}
            <div className="text-sm text-muted-foreground">
              Step {currentStep} of {steps.length}
            </div>

            {/* Next/Submit Button */}
            {currentStep < 3 ? (
              <Button
                type="button"
                onClick={handleNext}
                disabled={isValidating}
                className="gap-2 bg-primary hover:bg-primary/90"
              >
                {isValidating ? (
                  <>
                    Validating...
                    <Loader2 className="w-4 h-4 animate-spin" />
                  </>
                ) : (
                  <>
                    Next
                    <ChevronRight className="w-4 h-4" />
                  </>
                )}
              </Button>
            ) : (
              <Button
                type="button"
                onClick={(e) => {
                  e.preventDefault();
                  console.log("Button clicked, isSubmitting:", isSubmitting);
                  handleSubmit();
                }}
                disabled={isSubmitting}
                className="gap-2"
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Starting...
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4" />
                    Start Evaluation
                  </>
                )}
              </Button>
            )}
          </div>
        </div>
      </Card>

    </div>
  );
}
