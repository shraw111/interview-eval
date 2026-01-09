// TypeScript types matching backend Pydantic models

export interface CandidateInfo {
  name: string;
  current_level: string;
  target_level: string;
  years_experience: number;
  level_expectations: string;
}

export interface CreateEvaluationRequest {
  candidate_info: CandidateInfo;
  rubric: string;
  transcript: string;
}

export interface TokenMetadata {
  primary_evaluator_input: number;
  primary_evaluator_output: number;
  challenge_agent_input: number;
  challenge_agent_output: number;
  decision_agent_input: number;
  decision_agent_output: number;
  total_input: number;
  total_output: number;
  total: number;
}

export interface TimestampMetadata {
  start?: string;
  primary_evaluator?: string;
  challenge_agent?: string;
  decision_agent?: string;
}

export interface EvaluationMetadata {
  tokens: TokenMetadata;
  timestamps: TimestampMetadata;
  execution_time_seconds: number;
  cost_usd: number;
  model_version: string;
}

export interface EvaluationResult {
  candidate_info: CandidateInfo;
  primary_evaluation: string;
  challenges: string;
  final_evaluation: string;
  decision: string;
  metadata: EvaluationMetadata;
}

export type EvaluationStatus = "pending" | "processing" | "completed" | "failed";

export type AgentNode = "primary_evaluator" | "challenge_agent" | "decision_agent";

export interface EvaluationResponse {
  evaluation_id: string;
  status: EvaluationStatus;
  current_step?: AgentNode;
  progress_percentage: number;
  result?: EvaluationResult;
  error?: string;
  created_at: string;
  completed_at?: string;
  websocket_url?: string;
}

export interface EvaluationListItem {
  evaluation_id: string;
  candidate_name: string;
  status: EvaluationStatus;
  created_at: string;
  completed_at?: string;
}

export interface EvaluationListResponse {
  evaluations: EvaluationListItem[];
  total: number;
  limit: number;
  offset: number;
}
