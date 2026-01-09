"""Core evaluation service orchestrating LangGraph execution."""

import uuid
import asyncio
from datetime import datetime
from typing import Optional, Callable
from fastapi import BackgroundTasks

from ..models.requests import CreateEvaluationRequest
from ..models.responses import EvaluationResponse, EvaluationListItem
from ..utils.graph_executor import GraphExecutor
from .storage_service import storage


class EvaluationService:
    """Service for managing evaluations and executing the LangGraph workflow."""

    def __init__(self):
        """Initialize the evaluation service."""
        self.storage = storage
        # WebSocket manager will be injected later
        self.websocket_manager: Optional[Callable] = None

    def set_websocket_manager(self, manager: Callable):
        """Set the WebSocket manager for event broadcasting.

        Args:
            manager: WebSocket manager instance with emit method
        """
        self.websocket_manager = manager

    async def create_evaluation(
        self,
        request: CreateEvaluationRequest,
        background_tasks: BackgroundTasks
    ) -> EvaluationResponse:
        """Create a new evaluation and start processing.

        Args:
            request: Evaluation request data
            background_tasks: FastAPI background tasks handler

        Returns:
            Initial evaluation response with ID and status
        """
        # Generate unique ID
        evaluation_id = str(uuid.uuid4())

        # Store initial state
        initial_data = {
            "evaluation_id": evaluation_id,
            "status": "pending",
            "progress_percentage": 0,
            "created_at": datetime.now().isoformat(),
            "input": {
                "candidate_info": request.candidate_info.model_dump(),
                "rubric": request.rubric,
                "transcript": request.transcript
            },
            "result": None,
            "error": None
        }
        await self.storage.save(evaluation_id, initial_data)

        # Start background task for execution
        background_tasks.add_task(
            self._execute_evaluation_background,
            evaluation_id,
            request
        )

        # Return response
        return EvaluationResponse(
            evaluation_id=evaluation_id,
            status="pending",
            progress_percentage=0,
            created_at=initial_data["created_at"],
            websocket_url=f"ws://localhost:8000/ws/evaluations/{evaluation_id}"
        )

    async def _execute_evaluation_background(
        self,
        evaluation_id: str,
        request: CreateEvaluationRequest
    ):
        """Background task to execute the evaluation graph.

        Args:
            evaluation_id: Unique identifier for the evaluation
            request: Evaluation request data
        """
        try:
            # Update status to processing
            eval_data = await self.storage.get(evaluation_id)
            if eval_data:
                eval_data["status"] = "processing"
                await self.storage.save(evaluation_id, eval_data)

            # Create graph executor with event emitter
            executor = GraphExecutor(event_emitter=self._emit_websocket_event)

            # Execute the graph (this will use your existing LangGraph from src/graph/graph.py)
            start_time = datetime.now()
            final_state = await executor.execute_graph(
                evaluation_id=evaluation_id,
                rubric=request.rubric,
                transcript=request.transcript,
                candidate_info=request.candidate_info.model_dump()
            )
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()

            # Update final state with execution time
            if "metadata" in final_state:
                final_state["metadata"]["execution_time_seconds"] = execution_time

            # Store completed evaluation
            eval_data = await self.storage.get(evaluation_id)
            if eval_data:
                eval_data["status"] = "completed"
                eval_data["progress_percentage"] = 100
                eval_data["result"] = final_state
                eval_data["completed_at"] = end_time.isoformat()
                await self.storage.save(evaluation_id, eval_data)

        except Exception as e:
            # Handle errors
            error_message = str(e)
            eval_data = await self.storage.get(evaluation_id)
            if eval_data:
                eval_data["status"] = "failed"
                eval_data["error"] = error_message
                await self.storage.save(evaluation_id, eval_data)

            # Emit error event via WebSocket
            if self.websocket_manager:
                await self._emit_websocket_event(
                    evaluation_id,
                    {
                        "type": "error",
                        "error": error_message,
                        "timestamp": datetime.now().isoformat()
                    }
                )

    async def _emit_websocket_event(self, evaluation_id: str, event_data: dict):
        """Emit WebSocket event to connected clients.

        Args:
            evaluation_id: ID of the evaluation
            event_data: Event data to broadcast
        """
        if self.websocket_manager:
            await self.websocket_manager.broadcast(evaluation_id, event_data)

    async def get_evaluation(self, evaluation_id: str) -> Optional[EvaluationResponse]:
        """Get evaluation status and results.

        Args:
            evaluation_id: Unique identifier for the evaluation

        Returns:
            Evaluation response if found, None otherwise
        """
        eval_data = await self.storage.get(evaluation_id)
        if not eval_data:
            return None

        return EvaluationResponse(
            evaluation_id=eval_data["evaluation_id"],
            status=eval_data["status"],
            progress_percentage=eval_data.get("progress_percentage", 0),
            result=eval_data.get("result"),
            error=eval_data.get("error"),
            created_at=eval_data["created_at"],
            completed_at=eval_data.get("completed_at")
        )

    async def list_evaluations(
        self,
        limit: int = 20,
        offset: int = 0
    ) -> tuple[list[EvaluationListItem], int]:
        """List all evaluations with pagination.

        Args:
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            Tuple of (evaluation list, total count)
        """
        all_evals, total = await self.storage.list_all(limit, offset)

        items = []
        for eval_data in all_evals:
            candidate_info = eval_data.get("input", {}).get("candidate_info", {})
            items.append(
                EvaluationListItem(
                    evaluation_id=eval_data["evaluation_id"],
                    candidate_name=candidate_info.get("name", "Unknown"),
                    status=eval_data["status"],
                    created_at=eval_data["created_at"],
                    completed_at=eval_data.get("completed_at")
                )
            )

        return items, total


# Global instance (singleton pattern)
evaluation_service = EvaluationService()
