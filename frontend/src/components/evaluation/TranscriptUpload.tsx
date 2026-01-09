"use client";

import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { UseFormReturn } from "react-hook-form";
import { EvaluationFormData } from "@/lib/validation/schemas";
import { Upload } from "lucide-react";
import { useRef } from "react";

interface TranscriptUploadProps {
  form: UseFormReturn<EvaluationFormData>;
}

export function TranscriptUpload({ form }: TranscriptUploadProps) {
  const {
    register,
    watch,
    setValue,
    formState: { errors },
  } = form;

  const fileInputRef = useRef<HTMLInputElement>(null);
  const transcript = watch("transcript") || "";
  const charCount = transcript.length;

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const text = event.target?.result as string;
        setValue("transcript", text, { shouldValidate: true });
      };
      reader.readAsText(file);
    }
  };

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <Label>Interview Transcript *</Label>
        <span className="text-sm text-muted-foreground">
          {charCount.toLocaleString()} characters
        </span>
      </div>

      <Tabs defaultValue="paste" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="paste">Paste Text</TabsTrigger>
          <TabsTrigger value="upload">Upload File</TabsTrigger>
        </TabsList>

        <TabsContent value="paste" className="space-y-2">
          <Textarea
            rows={25}
            placeholder="Paste the interview transcript here...

Example format:
Interviewer: Can you walk me through a recent project where you had to influence stakeholders?

Candidate: Sure, I recently led the launch of our new analytics dashboard. The challenge was..."
            className="font-mono text-sm"
            {...register("transcript")}
          />
        </TabsContent>

        <TabsContent value="upload" className="space-y-4">
          <div className="border-2 border-dashed rounded-lg p-8 text-center">
            <Upload className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
            <p className="text-sm text-muted-foreground mb-4">
              Upload a .txt or .md file
            </p>
            <Button
              type="button"
              variant="outline"
              onClick={() => fileInputRef.current?.click()}
            >
              Choose File
            </Button>
            <input
              ref={fileInputRef}
              type="file"
              accept=".txt,.md"
              className="hidden"
              onChange={handleFileUpload}
            />
          </div>
          {transcript && (
            <div className="p-4 bg-muted rounded-lg">
              <p className="text-sm font-medium mb-2">Preview:</p>
              <p className="text-xs text-muted-foreground line-clamp-3">
                {transcript.substring(0, 200)}...
              </p>
            </div>
          )}
        </TabsContent>
      </Tabs>

      {errors.transcript && (
        <p className="text-sm text-red-500">{errors.transcript.message}</p>
      )}
      {charCount > 100000 && (
        <p className="text-sm text-amber-600">
          Very long transcript ({charCount.toLocaleString()} chars). This may take longer to process.
        </p>
      )}
    </div>
  );
}
