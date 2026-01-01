"""
LangGraph workflow definition with 4-node linear flow.
"""

from langgraph.graph import StateGraph, END
from .state import EvaluationState
from .nodes import (
    primary_evaluator_node,
    challenge_agent_node,
    primary_response_node,
    decision_agent_node
)


def create_evaluation_graph() -> StateGraph:
    """
    Create the 4-node evaluation workflow graph.

    Flow: primary → challenge → response → decision → END

    Returns:
        Compiled StateGraph ready for execution
    """
    workflow = StateGraph(EvaluationState)

    # Add all 4 nodes
    workflow.add_node("primary_evaluator", primary_evaluator_node)
    workflow.add_node("challenge_agent", challenge_agent_node)
    workflow.add_node("primary_response", primary_response_node)
    workflow.add_node("decision_agent", decision_agent_node)

    # Define linear flow
    workflow.set_entry_point("primary_evaluator")
    workflow.add_edge("primary_evaluator", "challenge_agent")
    workflow.add_edge("challenge_agent", "primary_response")
    workflow.add_edge("primary_response", "decision_agent")
    workflow.add_edge("decision_agent", END)

    return workflow.compile()


# Create singleton graph instance
evaluation_graph = create_evaluation_graph()
