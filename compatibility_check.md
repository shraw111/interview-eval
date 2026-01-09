# Compatibility Check: Improved Primary Agent Prompt

## What Changed

### Format Changes
**Original prompt output (per criterion):**
- Separate THOUGHT section
- Separate ACTION section with detailed evidence sub-bullets
- Separate OBSERVATION section (6 sub-items)
- Separate REFLECTION section
- Separate PRE-EMPTIVE DEFENSE section

**Improved prompt output (per criterion):**
- Combined "What This Criterion Requires" (thought)
- Supporting Evidence (streamlined)
- Counter-Evidence
- Score + Confidence (one line)
- Reasoning (2-3 sentences)
- Vulnerable Point (defense)

### Content Changes
- Removed hardcoded 1-5 scoring definitions → Now defers to rubric
- Simplified evidence format → Still includes quotes and what they demonstrate
- Reduced "we" vs "I" mentions → Still checks for it in counter-evidence
- Made weighted scoring conditional → Handles rubrics without weights
- Streamlined tables → Still includes all essential information

## What Challenge Agent Needs (from nodes.py:157-163)

The challenge agent is instructed to focus on:

1. **Critical criteria below required score**
   - ✅ Improved prompt outputs: Scores per criterion + Critical Criteria table

2. **Evidence-score mismatches**
   - ✅ Improved prompt outputs: Evidence quotes + Scores + Reasoning

3. **"I" vs "We" attribution issues**
   - ✅ Improved prompt outputs: Evidence quotes in Supporting/Counter-Evidence sections

4. **Activity vs outcome gaps**
   - ✅ Improved prompt outputs: Counter-Evidence section flags this

5. **Internal inconsistencies**
   - ✅ Improved prompt outputs: Reasoning per criterion + Final scores table

6. **Level appropriateness**
   - ✅ Improved prompt outputs: Assessment in Calibration Check section

## Integration Points

### How Primary Prompt is Used

**From src/graph/nodes.py:**

```python
# Line 47: Load active prompt
system_prompt = prompt_manager.get_active_prompt("primary_agent")

# Line 84-90: Call API with prompt
evaluation_text, input_tokens, output_tokens = call_anthropic_claude(
    model_name=...,
    system_prompt=system_prompt,  # Our improved prompt
    user_message=user_message,     # Context + rubric + transcript
    ...
)

# Line 99: Store result
return {
    "primary_evaluation": evaluation_text,  # Full text output
    ...
}
```

**From src/graph/nodes.py (Challenge Agent):**

```python
# Line 139: Challenge agent receives full text
user_message = f"""## PRIMARY EVALUATOR'S ASSESSMENT TO REVIEW

{state['primary_evaluation']}  # <-- Full output from improved prompt

---

## ORIGINAL TRANSCRIPT (for reference)
{state['transcript']}
...
"""
```

### No Hardcoded Parsing

✅ **Good news:** The system does NOT parse specific fields from the output.

- It passes the full text to challenge agent as-is
- Challenge agent reads it as a human would
- No JSON parsing, no regex extraction, no brittle field lookups

This means:
- Format changes are safe (as long as information is present)
- Simplified structure won't break anything
- Challenge agent can understand both verbose and concise formats

## What Could Break? (Analysis)

### Scenario 1: Missing Information
**Risk:** If improved prompt doesn't output something challenge agent needs
**Status:** ✅ SAFE - All required information is present:
- Scores ✓
- Evidence ✓
- Reasoning ✓
- Critical criteria ✓
- Confidence levels ✓

### Scenario 2: Unreadable Format
**Risk:** If output is so different challenge agent can't understand it
**Status:** ✅ SAFE - Still uses clear markdown sections with headers
- `### Criterion X: [Name]`
- `**Score: X/5**`
- `**Supporting Evidence:**`
- Tables still formatted as markdown tables

### Scenario 3: Changed Semantics
**Risk:** If scoring philosophy changes (e.g., different scale)
**Status:** ✅ SAFE - Actually IMPROVED:
- Removed hardcoded 1-5 assumptions
- Now respects whatever scale rubric defines
- More flexible, not less

### Scenario 4: Verbose vs Concise
**Risk:** Less verbosity = less information for challenge agent?
**Status:** ✅ SAFE - Reduced redundancy, not content:
- Still has evidence quotes
- Still has counter-evidence
- Still has reasoning
- Just removed repetitive sub-bullets

## Compatibility Verdict

✅ **FULLY COMPATIBLE**

The improved prompt:
1. Outputs all information the challenge agent expects
2. Uses similar markdown structure (headers, tables, bullets)
3. Actually improves compatibility by removing hardcoded assumptions
4. No downstream parsing will break (because there is none)

## Testing Recommendation

**Option 1: Direct Replacement (Recommended)**
- Replace active version in versions.json
- Challenge agent will receive more concise but complete output
- Should work immediately

**Option 2: A/B Test**
- Keep version 2 active
- Add improved prompt as version 3
- Test with a sample evaluation
- Compare outputs side-by-side
- Switch active version if satisfied

## How to Deploy

### Update versions.json

Add improved prompt as version 3:

```python
from src.prompts.manager import PromptManager

pm = PromptManager()

# Read improved prompt
with open('primary_agent_prompt_improved.txt', 'r', encoding='utf-8') as f:
    improved_content = f.read()

# Save as new version
new_version = pm.save_new_version(
    prompt_type="primary_agent",
    content=improved_content,
    notes="Streamlined version - removed hardcoded scoring, reduced verbosity, improved rubric flexibility",
    set_active=True  # Set to True to activate immediately
)

print(f"Created version {new_version}")
```

### Rollback if Needed

```python
# Revert to version 2 if issues arise
pm.set_active_version("primary_agent", "2")
```

## Summary

**Breaking Changes:** None

**Information Loss:** None

**Compatibility:** 100%

**Risk Level:** Low

**Recommendation:** Safe to deploy. The improved prompt is a strict improvement - more flexible, more concise, but maintains all essential information for the challenge agent to do its job.
