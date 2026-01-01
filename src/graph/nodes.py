"""
LangGraph node implementations with Anthropic Claude integration.
"""

import os
import yaml
from datetime import datetime
from typing import Dict, Any

from .state import EvaluationState
from ..prompts.manager import PromptManager
from ..utils.azure_client import call_anthropic_claude, calculate_cost


# Initialize prompt manager
prompt_manager = PromptManager()

# Load config
config_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "config.yaml"
)
with open(config_path, "r") as f:
    config = yaml.safe_load(f)


def primary_evaluator_node(state: EvaluationState) -> Dict[str, Any]:
    """
    Node 1: Primary evaluator conducts initial assessment.

    Args:
        state: Current evaluation state

    Returns:
        Dictionary with updates to state (primary_evaluation, metadata)
    """
    import sys
    import time

    node_start = time.time()
    sys.stderr.write("\n" + "="*60 + "\n")
    sys.stderr.write("[PRIMARY EVALUATOR NODE] Starting...\n")
    sys.stderr.flush()

    # Get active prompt
    prompt_start = time.time()
    system_prompt = prompt_manager.get_active_prompt("primary_agent")
    sys.stderr.write(f"[PRIMARY] Loaded prompt in {time.time() - prompt_start:.2f}s\n")
    sys.stderr.flush()

    # Build user message
    user_message = f"""## EVALUATION CONTEXT

**Current Level:** {state['candidate_info']['current_level']}
**Target Level:** {state['candidate_info']['target_level']}

**What Distinguishes Target from Current Level:**
{state['candidate_info']['level_expectations']}

---

## EVALUATION CRITERIA (RUBRIC)

{state['rubric']}

---

## INTERVIEW TRANSCRIPT

{state['transcript']}

---

## YOUR TASK

Evaluate this candidate using the ReAct framework. For each criterion in the rubric, follow the THOUGHT → ACTION → OBSERVATION → REFLECTION cycle, then provide final scores and recommendation.
"""

    # Call Anthropic Claude
    model_config = config["models"]["primary_agent"]
    sys.stderr.write(f"[PRIMARY] Calling API with max_tokens={model_config['max_tokens']}...\n")
    sys.stderr.flush()

    evaluation_text, input_tokens, output_tokens = call_anthropic_claude(
        model_name=model_config["model_name"],
        system_prompt=system_prompt,
        user_message=user_message,
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"]
    )

    node_duration = time.time() - node_start
    sys.stderr.write(f"[PRIMARY] COMPLETE - Total node time: {node_duration:.2f}s\n")
    sys.stderr.write("="*60 + "\n\n")
    sys.stderr.flush()

    # Return updates
    return {
        "primary_evaluation": evaluation_text,
        "metadata": {
            **state["metadata"],
            "tokens": {
                **state["metadata"]["tokens"],
                "primary_input": input_tokens,
                "primary_output": output_tokens
            },
            "timestamps": {
                **state["metadata"]["timestamps"],
                "primary": datetime.now().isoformat()
            }
        }
    }


def challenge_agent_node(state: EvaluationState) -> Dict[str, Any]:
    """
    Node 2: Challenge agent reviews primary evaluation.

    Args:
        state: Current evaluation state

    Returns:
        Dictionary with updates to state (challenges, metadata)
    """
    import sys
    import time

    node_start = time.time()
    sys.stderr.write("\n" + "="*60 + "\n")
    sys.stderr.write("[CHALLENGE AGENT NODE] Starting...\n")
    sys.stderr.flush()

    # Get active prompt
    system_prompt = prompt_manager.get_active_prompt("challenge_agent")

    # Build user message
    user_message = f"""## PRIMARY EVALUATOR'S ASSESSMENT TO REVIEW

{state['primary_evaluation']}

---

## ORIGINAL TRANSCRIPT (for reference)

{state['transcript']}

---

## RUBRIC (to check critical criteria)

{state['rubric']}

---

## YOUR TASK

Review the primary evaluation and generate challenges. Focus on:
1. Critical criteria below required score
2. Evidence-score mismatches
3. "I" vs "We" attribution issues
4. Activity vs outcome gaps
5. Internal inconsistencies
6. Level appropriateness
"""

    # Call Anthropic Claude
    model_config = config["models"]["challenge_agent"]
    sys.stderr.write(f"[CHALLENGE] Calling API with max_tokens={model_config['max_tokens']}...\n")
    sys.stderr.flush()

    challenges_text, input_tokens, output_tokens = call_anthropic_claude(
        model_name=model_config["model_name"],
        system_prompt=system_prompt,
        user_message=user_message,
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"]
    )

    node_duration = time.time() - node_start
    sys.stderr.write(f"[CHALLENGE] COMPLETE - Total node time: {node_duration:.2f}s\n")
    sys.stderr.write("="*60 + "\n\n")
    sys.stderr.flush()

    # Return updates
    return {
        "challenges": challenges_text,
        "metadata": {
            **state["metadata"],
            "tokens": {
                **state["metadata"]["tokens"],
                "challenge_input": input_tokens,
                "challenge_output": output_tokens
            },
            "timestamps": {
                **state["metadata"]["timestamps"],
                "challenge": datetime.now().isoformat()
            }
        }
    }


def primary_response_node(state: EvaluationState) -> Dict[str, Any]:
    """
    Node 3: Primary evaluator responds to challenges.

    Args:
        state: Current evaluation state

    Returns:
        Dictionary with updates to state (final_evaluation, metadata)
    """
    import sys
    import time

    node_start = time.time()
    sys.stderr.write("\n" + "="*60 + "\n")
    sys.stderr.write("[RESPONSE AGENT NODE] Starting...\n")
    sys.stderr.flush()

    # Get active prompt (same as primary)
    system_prompt = prompt_manager.get_active_prompt("primary_agent")

    # Build user message
    user_message = f"""## YOUR ORIGINAL EVALUATION

{state['primary_evaluation']}

---

## CHALLENGES FROM PEER REVIEWER

{state['challenges']}

---

## ORIGINAL TRANSCRIPT (for re-examination)

{state['transcript']}

---

## YOUR TASK

Respond to each challenge raised by the peer evaluator:

For each challenge:
1. **Re-examine the transcript** - Look again at the specific area questioned
2. **Decide:** DEFEND your original score with additional evidence OR REVISE if challenge is valid
3. **Explain** your reasoning clearly

Then provide your FINAL EVALUATION with:

## RESPONSES TO CHALLENGES

[For each challenge: Original score, Challenge summary, Your response, Decision (DEFEND/REVISE), Justification]

## FINAL SCORES (After Calibration)

[Complete table with all criteria - show which scores changed]

## SCORE CHANGES SUMMARY

[Table showing: Criterion | Initial | Revised | Reason]

## RECALCULATED WEIGHTED SCORE

[Show the math with new scores]

## UPDATED CRITICAL CRITERIA STATUS

[Check if any status changed]

## FINAL RECOMMENDATION

**Decision:** [STRONG RECOMMEND / RECOMMEND / BORDERLINE / DO NOT RECOMMEND]

**Rationale:** [Updated based on calibrated scores]

**Key Changes from Initial Assessment:**
[What changed during calibration and how it affected recommendation]

**Development Areas (if promoting):**
1. [Specific actionable area]
2. [Specific actionable area]
"""

    # Call Anthropic Claude
    model_config = config["models"]["response_agent"]
    sys.stderr.write(f"[RESPONSE] Calling API with max_tokens={model_config['max_tokens']}...\n")
    sys.stderr.flush()

    final_text, input_tokens, output_tokens = call_anthropic_claude(
        model_name=model_config["model_name"],
        system_prompt=system_prompt,
        user_message=user_message,
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"]
    )

    node_duration = time.time() - node_start
    sys.stderr.write(f"[RESPONSE] COMPLETE - Total node time: {node_duration:.2f}s\n")
    sys.stderr.write("="*60 + "\n\n")
    sys.stderr.flush()

    # Return updates (don't calculate totals yet - decision agent still needs to run)
    return {
        "final_evaluation": final_text,
        "metadata": {
            **state["metadata"],
            "tokens": {
                **state["metadata"]["tokens"],
                "final_input": input_tokens,
                "final_output": output_tokens
            },
            "timestamps": {
                **state["metadata"]["timestamps"],
                "final": datetime.now().isoformat()
            }
        }
    }


def decision_agent_node(state: EvaluationState) -> Dict[str, Any]:
    """
    Node 4: Decision agent makes final promotion recommendation.

    Args:
        state: Current evaluation state

    Returns:
        Dictionary with updates to state (decision, metadata with totals)
    """
    import sys
    import time

    node_start = time.time()
    sys.stderr.write("\n" + "="*60 + "\n")
    sys.stderr.write("[DECISION AGENT NODE] Starting...\n")
    sys.stderr.flush()

    # Get active prompt
    system_prompt = prompt_manager.get_active_prompt("decision_agent")

    # Build user message
    user_message = f"""## CALIBRATED EVALUATION (After Primary Response to Challenges)

{state['final_evaluation']}

---

## RUBRIC

{state['rubric']}

---

## CANDIDATE INFORMATION

**Name:** {state['candidate_info']['name']}
**Current Level:** {state['candidate_info']['current_level']}
**Target Level:** {state['candidate_info']['target_level']}
**Years at Current Level:** {state['candidate_info']['years_experience']}

**Level Expectations:**
{state['candidate_info']['level_expectations']}

---

## YOUR TASK

Review the calibrated evaluation and make a final promotion decision:

1. Extract the overall scores and identify critical criteria from the rubric
2. Conduct holistic assessment beyond just scores
3. Assess promotion risk
4. Make final decision: **STRONG RECOMMEND / RECOMMEND / BORDERLINE / DO NOT RECOMMEND**

Provide comprehensive rationale, key factors, development areas, and confidence level.
"""

    # Call Anthropic Claude
    model_config = config["models"]["decision_agent"]
    sys.stderr.write(f"[DECISION] Calling API with max_tokens={model_config['max_tokens']}...\n")
    sys.stderr.flush()

    decision_text, input_tokens, output_tokens = call_anthropic_claude(
        model_name=model_config["model_name"],
        system_prompt=system_prompt,
        user_message=user_message,
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"]
    )

    node_duration = time.time() - node_start
    sys.stderr.write(f"[DECISION] COMPLETE - Total node time: {node_duration:.2f}s\n")
    sys.stderr.write("="*60 + "\n\n")
    sys.stderr.flush()

    # Calculate totals now that all nodes have run
    start_time = datetime.fromisoformat(state["metadata"]["timestamps"]["start"])
    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()

    total_input = (
        state["metadata"]["tokens"]["primary_input"] +
        state["metadata"]["tokens"]["challenge_input"] +
        state["metadata"]["tokens"]["final_input"] +
        input_tokens
    )

    total_output = (
        state["metadata"]["tokens"]["primary_output"] +
        state["metadata"]["tokens"]["challenge_output"] +
        state["metadata"]["tokens"]["final_output"] +
        output_tokens
    )

    total_tokens = total_input + total_output
    total_cost = calculate_cost(total_input, total_output)

    # Return updates with final totals
    return {
        "decision": decision_text,
        "metadata": {
            **state["metadata"],
            "tokens": {
                **state["metadata"]["tokens"],
                "decision_input": input_tokens,
                "decision_output": output_tokens,
                "total": total_tokens
            },
            "timestamps": {
                **state["metadata"]["timestamps"],
                "decision": end_time.isoformat()
            },
            "execution_time_seconds": round(execution_time, 1),
            "cost_usd": round(total_cost, 2),
            "model_version": model_config["model_name"]
        }
    }
