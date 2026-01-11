import { apiClient } from "./client";
import {
  CreateEvaluationRequest,
  EvaluationResponse,
  EvaluationListResponse,
} from "@/types/evaluation";

export async function createEvaluation(
  data: CreateEvaluationRequest
): Promise<EvaluationResponse> {
  const response = await apiClient.post<EvaluationResponse>("/evaluations", data);
  return response.data;
}

export async function getEvaluation(
  evaluationId: string
): Promise<EvaluationResponse> {
  const response = await apiClient.get<EvaluationResponse>(
    `/evaluations/${evaluationId}`
  );
  return response.data;
}

export async function listEvaluations(
  limit: number = 20,
  offset: number = 0
): Promise<EvaluationListResponse> {
  const response = await apiClient.get<EvaluationListResponse>("/evaluations", {
    params: { limit, offset },
  });
  return response.data;
}
