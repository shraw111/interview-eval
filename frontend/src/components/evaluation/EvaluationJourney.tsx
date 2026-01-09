"use client";

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { MarkdownRenderer } from "@/components/shared/MarkdownRenderer";
import { EvaluationResult } from "@/types/evaluation";
import { Clock, FileText, MessageSquare, RefreshCw, CheckCircle2, ChevronRight } from "lucide-react";

interface EvaluationJourneyProps {
  result: EvaluationResult;
}

export function EvaluationJourney({ result }: EvaluationJourneyProps) {
  const { primary_evaluation, challenges, final_evaluation, decision, metadata } = result;

  const getNodeDuration = (node: keyof typeof metadata.timestamps): string => {
    // This is a simplified version - in reality you'd calculate from timestamps
    return "45s";
  };

  const stages = [
    {
      id: "primary",
      title: "Initial Assessment",
      description: "Primary evaluator reviews transcript against rubric",
      content: primary_evaluation,
      icon: FileText,
      number: 1,
      duration: getNodeDuration("primary_evaluator"),
    },
    {
      id: "challenges",
      title: "Critical Review",
      description: "Challenger agent identifies gaps and biases",
      content: challenges,
      icon: MessageSquare,
      number: 2,
      duration: getNodeDuration("challenge_agent"),
    },
    {
      id: "decision",
      title: "Final Decision",
      description: "Decision agent calibrates scores and makes recommendation",
      content: decision,
      icon: CheckCircle2,
      number: 3,
      duration: getNodeDuration("decision_agent"),
      isHighlight: true,
    },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-semibold text-gray-900 mb-2">Evaluation Process</h2>
        <p className="text-sm text-gray-600">
          Review how each AI agent contributed to the final evaluation
        </p>
      </div>

      {/* Process Timeline */}
      <div className="relative">
        <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200" />
        <div className="space-y-6">
          {stages.map((stage, index) => (
            <div key={stage.id} className="relative flex gap-4">
              {/* Timeline Icon */}
              <div className="relative z-10 flex-shrink-0">
                <div className={`
                  w-8 h-8 rounded-full flex items-center justify-center
                  ${stage.isHighlight ? 'bg-primary text-white' : 'bg-white border-2 border-gray-300'}
                `}>
                  {stage.isHighlight ? (
                    <stage.icon className="w-4 h-4" />
                  ) : (
                    <span className="text-xs font-semibold text-gray-600">{stage.number}</span>
                  )}
                </div>
              </div>

              {/* Content Card */}
              <div className="flex-1 pb-6">
                <Accordion type="multiple" defaultValue={stage.isHighlight ? [stage.id] : []} className="w-full">
                  <AccordionItem
                    value={stage.id}
                    className={`
                      border rounded-lg bg-white shadow-card overflow-hidden
                      ${stage.isHighlight ? 'border-primary/30 ring-2 ring-primary/10' : 'border-gray-200'}
                    `}
                  >
                    <AccordionTrigger className="hover:no-underline px-5 py-4 hover:bg-gray-50 transition-colors">
                      <div className="flex items-start justify-between w-full text-left">
                        <div className="flex-1 pr-4">
                          <div className="flex items-center gap-2 mb-1">
                            <stage.icon className={`w-4 h-4 ${stage.isHighlight ? 'text-primary' : 'text-gray-400'}`} />
                            <h3 className="font-semibold text-gray-900">{stage.title}</h3>
                          </div>
                          <p className="text-sm text-gray-600">{stage.description}</p>
                          <div className="flex items-center gap-2 mt-2 text-xs text-gray-500">
                            <Clock className="w-3 h-3" />
                            <span>{stage.duration}</span>
                          </div>
                        </div>
                        <ChevronRight className="w-5 h-5 text-gray-400 flex-shrink-0 transition-transform group-data-[state=open]:rotate-90" />
                      </div>
                    </AccordionTrigger>

                    <AccordionContent className="px-5 pb-5 pt-2">
                      <div className="bg-gray-50 rounded-lg p-4 border border-gray-100">
                        <MarkdownRenderer content={stage.content} />
                      </div>
                    </AccordionContent>
                  </AccordionItem>
                </Accordion>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
