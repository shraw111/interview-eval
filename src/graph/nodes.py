"""
LangGraph node implementations with Anthropic Claude integration.
"""

import os
import yaml
import json
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


def format_rubric_as_json(rubric: str) -> str:
    """
    Format rubric as JSON string for GPT-5.2 optimal processing.
    If rubric is already valid JSON, return it as-is (pretty-printed).
    If it's text/markdown, wrap it in a simple JSON structure.

    Args:
        rubric: Rubric string (JSON or text format)

    Returns:
        JSON-formatted rubric string
    """
    try:
        # Try to parse as JSON first
        rubric_obj = json.loads(rubric)
        # Already JSON, return pretty-printed version
        return json.dumps(rubric_obj, indent=2)
    except json.JSONDecodeError:
        # Not JSON, wrap text rubric in simple JSON structure
        return json.dumps({
            "rubric_format": "text",
            "content": rubric
        }, indent=2)


def extract_json_from_response(response_text: str) -> tuple[dict, str]:
    """
    Extract JSON block from decision agent response.
    Handles both code-fenced JSON and raw JSON.

    Args:
        response_text: Full response from decision agent

    Returns:
        Tuple of (parsed_json_dict, remaining_text)
    """
    import re
    import sys

    expected_criteria = [
        "Overall Presentation Quality", "Presentation Structure", "Storytelling Skills",
        "Problem Statement", "Opportunity Sizing", "Depth of Research",
        "Current Business Model Definition", "Business Analysis",
        "Target Business Model Alternatives", "Criteria for Selection",
        "GTM Approach", "Vision & Roadmap", "Implementation Plan", "Prototype Creation"
    ]

    # Strategy 1: Try to find JSON block in code fence
    json_pattern = r'```json\s*\n(.*?)\n```'
    match = re.search(json_pattern, response_text, re.DOTALL)

    if match:
        sys.stderr.write("[DECISION] Found JSON in code fence\n")
        sys.stderr.flush()
        json_str = match.group(1)
        try:
            parsed_json = json.loads(json_str)
            remaining_text = response_text[:match.start()] + response_text[match.end():]
            remaining_text = remaining_text.strip()
            sys.stderr.write(f"[DECISION] Extracted JSON successfully (code fence)\n")
            sys.stderr.write(f"[DECISION] Narrative text length: {len(remaining_text)} chars\n")
            sys.stderr.flush()
            return parsed_json, remaining_text
        except json.JSONDecodeError as e:
            sys.stderr.write(f"[DECISION] JSON decode error (code fence): {e}\n")
            sys.stderr.flush()

    # Strategy 2: Find JSON by looking for the complete structure starting with { and ending with }
    # Look for a JSON object that contains "decision" and "comparison_rows"
    sys.stderr.write("[DECISION] Trying to find raw JSON structure...\n")
    sys.stderr.flush()

    # Find all potential JSON blocks (opening { to closing })
    brace_depth = 0
    start_idx = -1
    potential_jsons = []

    for i, char in enumerate(response_text):
        if char == '{':
            if brace_depth == 0:
                start_idx = i
            brace_depth += 1
        elif char == '}':
            brace_depth -= 1
            if brace_depth == 0 and start_idx != -1:
                potential_jsons.append((start_idx, i + 1))
                start_idx = -1

    sys.stderr.write(f"[DECISION] Found {len(potential_jsons)} potential JSON blocks\n")
    sys.stderr.flush()

    # Try to parse each potential JSON block
    for start, end in potential_jsons:
        json_str = response_text[start:end]
        try:
            parsed_json = json.loads(json_str)

            # Check if it has the expected structure
            if "decision" in parsed_json and "comparison_rows" in parsed_json:
                sys.stderr.write(f"[DECISION] Found valid JSON structure at position {start}-{end}\n")
                sys.stderr.flush()

                # Validate comparison_rows
                rows = parsed_json.get("comparison_rows", [])
                sys.stderr.write(f"[DECISION] JSON has {len(rows)} comparison rows\n")
                sys.stderr.flush()

                # Remove JSON from text
                remaining_text = response_text[:start] + response_text[end:]
                remaining_text = remaining_text.strip()

                # Clean up any JSON remnants
                remaining_text = re.sub(r'\{[^}]*"Criterion"[^}]*\}', '', remaining_text)
                remaining_text = re.sub(r'^\s*[\{\}]\s*$', '', remaining_text, flags=re.MULTILINE)
                remaining_text = '\n'.join(line for line in remaining_text.split('\n') if line.strip())

                sys.stderr.write(f"[DECISION] Successfully extracted JSON\n")
                sys.stderr.write(f"[DECISION] Narrative text length after cleaning: {len(remaining_text)} chars\n")
                sys.stderr.flush()

                return parsed_json, remaining_text

        except json.JSONDecodeError:
            continue

    # No valid JSON found
    sys.stderr.write("[DECISION] Warning: No valid JSON found in response\n")
    sys.stderr.write(f"[DECISION] Response preview: {response_text[:200]}...\n")
    sys.stderr.flush()
    return {}, response_text


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

    # Format rubric as JSON
    rubric_json = format_rubric_as_json(state['rubric'])

    # Build user message with optional level context
    level_context = ""
    if state['candidate_info'].get('current_level') or state['candidate_info'].get('target_level'):
        level_context = f"""## EVALUATION CONTEXT

**Current Level:** {state['candidate_info'].get('current_level', 'N/A')}
**Target Level:** {state['candidate_info'].get('target_level', 'N/A')}
"""
        if state['candidate_info'].get('level_expectations'):
            level_context += f"""
**What Distinguishes Target from Current Level:**
{state['candidate_info']['level_expectations']}
"""
        level_context += "\n---\n\n"

    user_message = f"""{level_context}## EVALUATION CRITERIA (RUBRIC)

```json
{rubric_json}
```

---

## INTERVIEW TRANSCRIPT

{state['transcript']}

---

## YOUR TASK

Evaluate this candidate based on the rubric above. For each criterion, provide evidence-based scoring following the format specified in your system prompt.
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

    # Format rubric as JSON
    rubric_json = format_rubric_as_json(state['rubric'])

    # Build user message
    user_message = f"""## PRIMARY EVALUATOR'S ASSESSMENT TO REVIEW

{state['primary_evaluation']}

---

## ORIGINAL TRANSCRIPT (for reference)

{state['transcript']}

---

## RUBRIC (to check critical criteria)

```json
{rubric_json}
```

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


def decision_agent_node(state: EvaluationState) -> Dict[str, Any]:
    """
    Node 3: Unified decision agent - defends/calibrates AND makes final decision.

    This agent:
    1. Receives original evaluation + challenges + transcript
    2. Responds to each challenge (DEFEND or REVISE)
    3. Produces calibrated final scores
    4. Makes final promotion decision

    Args:
        state: Current evaluation state

    Returns:
        Dictionary with updates to state (final_evaluation, decision, metadata with totals)
    """
    import sys
    import time

    node_start = time.time()
    sys.stderr.write("\n" + "="*60 + "\n")
    sys.stderr.write("[DECISION AGENT NODE] Starting...\n")
    sys.stderr.flush()

    # Get active prompt (use updated decision_agent prompt)
    system_prompt = prompt_manager.get_active_prompt("decision_agent")

    # Format rubric as JSON
    rubric_json = format_rubric_as_json(state['rubric'])

    # Build user message with context data (instructions come from system prompt)
    user_message = f"""## PRIMARY AGENT EVALUATION
{state['primary_evaluation']}

---

## CHALLENGER AGENT REVIEW
{state['challenges']}

---

## INTERVIEW TRANSCRIPT
{state['transcript']}

---

## EVALUATION RUBRIC
```json
{rubric_json}
```

---

## CANDIDATE INFORMATION
**Name:** {state['candidate_info']['name']}
{f"**Current Level:** {state['candidate_info']['current_level']}" if state['candidate_info'].get('current_level') else ""}
{f"**Target Level:** {state['candidate_info']['target_level']}" if state['candidate_info'].get('target_level') else ""}
{f"**Years at Current Level:** {state['candidate_info']['years_experience']}" if state['candidate_info'].get('years_experience') is not None else ""}
{f"**Level Expectations:**\\n{state['candidate_info']['level_expectations']}" if state['candidate_info'].get('level_expectations') else ""}
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

    # Extract JSON from response (v5 prompt returns JSON first)
    decision_json, narrative_text = extract_json_from_response(decision_text)

    if decision_json:
        sys.stderr.write(f"[DECISION] Successfully extracted JSON with {len(decision_json.get('comparison_rows', []))} comparison rows\n")
        sys.stderr.flush()
    else:
        sys.stderr.write(f"[DECISION] Warning: No JSON found in response, using raw text\n")
        sys.stderr.flush()

    # Calculate totals now that all nodes have run
    start_time = datetime.fromisoformat(state["metadata"]["timestamps"]["start"])
    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()

    total_input = (
        state["metadata"]["tokens"]["primary_input"] +
        state["metadata"]["tokens"]["challenge_input"] +
        input_tokens
    )

    total_output = (
        state["metadata"]["tokens"]["primary_output"] +
        state["metadata"]["tokens"]["challenge_output"] +
        output_tokens
    )

    total_tokens = total_input + total_output
    total_cost = calculate_cost(total_input, total_output)

    # Return updates - include both structured JSON and full text
    return {
        "final_evaluation": decision_text,  # Keep for backward compatibility - full text
        "decision": narrative_text if narrative_text else decision_text,  # Narrative only
        "decision_json": decision_json if decision_json else {},  # Structured JSON data
        "metadata": {
            **state["metadata"],
            "tokens": {
                **state["metadata"]["tokens"],
                "decision_input": input_tokens,
                "decision_output": output_tokens,
                "total_input": total_input,
                "total_output": total_output,
                "total": total_tokens
            },
            "timestamps": {
                **state["metadata"]["timestamps"],
                "decision": datetime.now().isoformat()
            },
            "total_cost_usd": total_cost,
            "execution_time_seconds": execution_time
        }
    }
