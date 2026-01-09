"""Wrapper for executing LangGraph with WebSocket progress streaming."""

import sys
import os
import asyncio
import logging
from datetime import datetime
from typing import Callable, Optional, Dict, Any

# Add parent directories to path to import from src/
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from src.graph.graph import evaluation_graph
from src.graph.state import create_initial_state, EvaluationState


logger = logging.getLogger(__name__)


class GraphExecutor:
    """Executes the evaluation graph with progress hooks for WebSocket streaming."""

    # Map node names to progress percentages
    PROGRESS_MAP = {
        "primary_evaluator": {"started": 0, "completed": 33},
        "challenge_agent": {"started": 33, "completed": 67},
        "decision_agent": {"started": 67, "completed": 100}
    }

    def __init__(self, event_emitter: Optional[Callable[[str, dict], None]] = None):
        """Initialize graph executor.

        Args:
            event_emitter: Optional callback function to emit events (evaluation_id, event_data)
        """
        self.event_emitter = event_emitter

    async def emit_event(self, evaluation_id: str, event_type: str, **kwargs):
        """Emit a WebSocket event if emitter is configured.

        Args:
            evaluation_id: ID of the evaluation
            event_type: Type of event (node_started, node_completed, etc.)
            **kwargs: Additional event data
        """
        if self.event_emitter:
            event_data = {
                "type": event_type,
                "timestamp": datetime.now().isoformat(),
                **kwargs
            }
            await self.event_emitter(evaluation_id, event_data)

    async def execute_graph(
        self,
        evaluation_id: str,
        rubric: str,
        transcript: str,
        candidate_info: dict
    ) -> Dict[str, Any]:
        """Execute the evaluation graph with progress streaming.

        Args:
            evaluation_id: Unique identifier for this evaluation
            rubric: Natural language evaluation criteria
            transcript: Interview transcript
            candidate_info: Candidate information dict

        Returns:
            Final evaluation state as dictionary

        Raises:
            Exception: If graph execution fails
        """
        # Create initial state using existing function
        initial_state = create_initial_state(
            rubric=rubric,
            transcript=transcript,
            candidate_info=candidate_info
        )

        # Emit evaluation started event
        await self.emit_event(evaluation_id, "evaluation_started")

        # Async queue for event communication
        event_queue = asyncio.Queue()

        def run_graph_in_thread(loop):
            """Synchronous function to run graph in thread pool."""
            current_state = dict(initial_state)

            def put_event_sync(event):
                """Put event into async queue from sync context."""
                asyncio.run_coroutine_threadsafe(event_queue.put(event), loop)

            try:
                # Stream through the graph (blocking operation)
                for chunk in evaluation_graph.stream(initial_state, stream_mode="updates"):
                    for node_name, node_output in chunk.items():
                        # Signal node started
                        if node_name in self.PROGRESS_MAP:
                            progress = self.PROGRESS_MAP[node_name]["started"]
                            put_event_sync(("node_started", node_name, progress))

                        # Merge node output into current state
                        for key, value in node_output.items():
                            if isinstance(value, dict) and isinstance(current_state.get(key), dict):
                                current_state[key] = {**current_state[key], **value}
                            else:
                                current_state[key] = value

                        # Signal node completed with current state snapshot
                        if node_name in self.PROGRESS_MAP:
                            progress = self.PROGRESS_MAP[node_name]["completed"]
                            # Create a deep copy of state for this event
                            state_snapshot = {
                                "metadata": current_state.get("metadata", {}),
                                "primary_evaluation": current_state.get("primary_evaluation", ""),
                                "challenges": current_state.get("challenges", ""),
                                "final_evaluation": current_state.get("final_evaluation", ""),
                                "decision": current_state.get("decision", "")
                            }
                            put_event_sync(("node_completed", node_name, progress, state_snapshot))

                # Signal completion
                put_event_sync(("completed", current_state))
                return current_state

            except Exception as e:
                put_event_sync(("error", str(e)))
                raise

        # Get current event loop
        loop = asyncio.get_event_loop()

        # Start graph execution in thread pool
        graph_task = asyncio.create_task(asyncio.to_thread(run_graph_in_thread, loop))

        # Process events from queue while graph runs
        final_state = None
        try:
            while True:
                # Check for events with timeout (non-blocking async)
                try:
                    event = await asyncio.wait_for(event_queue.get(), timeout=0.5)

                    if event[0] == "node_started":
                        _, node_name, progress = event
                        await self.emit_event(
                            evaluation_id,
                            "node_started",
                            node=node_name,
                            progress_percentage=progress
                        )

                    elif event[0] == "node_completed":
                        _, node_name, progress, state_snapshot = event

                        # Extract token info
                        tokens = None
                        if state_snapshot.get("metadata", {}).get("tokens"):
                            token_data = state_snapshot["metadata"]["tokens"]
                            tokens = {
                                "input": token_data.get(f"{node_name}_input", 0),
                                "output": token_data.get(f"{node_name}_output", 0)
                            }

                        # Get output preview
                        output_preview = None
                        if node_name == "primary_evaluator" and state_snapshot.get("primary_evaluation"):
                            output_preview = state_snapshot["primary_evaluation"][:200]
                        elif node_name == "challenge_agent" and state_snapshot.get("challenges"):
                            output_preview = state_snapshot["challenges"][:200]
                        elif node_name == "decision_agent" and state_snapshot.get("decision"):
                            output_preview = state_snapshot["decision"][:200]

                        await self.emit_event(
                            evaluation_id,
                            "node_completed",
                            node=node_name,
                            progress_percentage=progress,
                            output_preview=output_preview,
                            tokens=tokens
                        )

                    elif event[0] == "completed":
                        final_state = event[1]
                        await self.emit_event(
                            evaluation_id,
                            "evaluation_completed",
                            result=final_state
                        )
                        break

                    elif event[0] == "error":
                        error_msg = event[1]
                        await self.emit_event(
                            evaluation_id,
                            "error",
                            error=error_msg
                        )
                        break

                except asyncio.TimeoutError:
                    # No event in queue, check if task is done
                    if graph_task.done():
                        # Task finished, get result or exception
                        try:
                            final_state = await graph_task
                            if final_state and event_queue.empty():
                                # Task completed but no completion event received
                                logger.warning("Graph completed but no completion event received")
                                await self.emit_event(
                                    evaluation_id,
                                    "evaluation_completed",
                                    result=final_state
                                )
                        except Exception as e:
                            logger.error(f"Graph execution failed: {e}")
                            # Exception already put in queue, will be processed
                        break
                    # Continue polling

            # Wait for graph task to complete
            if not graph_task.done():
                final_state = await graph_task
            elif final_state is None:
                final_state = await graph_task

            return final_state

        except Exception as e:
            logger.error(f"Graph executor error: {e}")
            await self.emit_event(
                evaluation_id,
                "error",
                error=str(e)
            )
            raise
