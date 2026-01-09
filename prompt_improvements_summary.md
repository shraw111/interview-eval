# Primary Agent Prompt Improvements

## Summary of Changes

I've created an improved version of the primary agent prompt (`primary_agent_prompt_improved.txt`) that addresses key issues while maintaining evaluation rigor.

---

## Key Improvements

### 1. **Reduced Output Verbosity (~40% shorter output)**

**Before:**
- Separate THOUGHT/ACTION/OBSERVATION/REFLECTION sections with extensive sub-bullets
- Detailed evidence formatting with Context/Demonstrates/Assessment for each quote
- Multiple detailed self-check questions

**After:**
- Combined "THOUGHT & ACTION" into single section
- Streamlined evidence format: `"Quote" - [What this demonstrates]`
- Consolidated OBSERVATION + REFLECTION into one section
- Simplified calibration check with focused questions

**Impact:** Estimated output reduced from ~10,000+ tokens to ~6,000-7,000 tokens while maintaining all essential rigor.

---

### 2. **Fixed Weighted Scoring Assumption**

**Before (Lines 170-184):**
```
## WEIGHTED SCORE CALCULATION

[Calculate based on weights provided in rubric, if applicable]

**[Category 1 Name] ([X]% weight):**
- [Criterion A] ([Y]% weight): [Z]/[max]
...
**OVERALL WEIGHTED SCORE: X.XX/[max] (XX%)**

[If rubric doesn't use weighted scoring, adapt this section accordingly]
```

**After:**
```
## OVERALL SCORE

**If rubric specifies weights or percentages:**
Calculate weighted average and show breakdown by category.

**If rubric has no explicit weights:**
- Average Score: X.XX/[max] ([XX]%)
- Score Distribution: [How many 5s, 4s, 3s, 2s, 1s]
```

**Impact:** Agent now handles both weighted rubrics AND simple markdown rubrics without weights. No more forcing calculations that don't apply.

---

### 3. **Reduced "We" vs "I" Over-Emphasis**

**Before:** Mentioned 6+ times throughout prompt:
- Line 79: "Team achievements ("we") without personal contribution ("I")?"
- Line 89: "For interviews: Check personal contribution ("I") vs team achievement ("we")"
- Line 133: "[For interviews: "We" language without "I" contribution]"
- Line 142: "For interviews: Personal vs Team: [Clear "I" contributions / Mostly "We" / Unclear]"

**After:** Mentioned 2 times (kept where most relevant):
- In counter-evidence section: "Team achievements ("we") without clear personal contribution ("I")?"
- That's it - removed redundant mentions in OBSERVATION template

**Impact:** Guidance remains but isn't repetitive. Agent won't over-index on this single factor.

---

### 4. **Simplified Format Requirements**

**Before:**
- Prescriptive table formats with exact column headers
- Required sub-bullets for every evidence item (Context/Demonstrates/Assessment)
- Mandatory sections regardless of applicability
- Very specific markdown formatting requirements

**After:**
- Flexible table formats focused on essential information
- Simplified evidence bullets: Just quote + what it shows
- Conditional sections (e.g., "Only include this section if rubric specifies critical criteria")
- Focus on content over structure

**Impact:** Agent can adapt output to rubric complexity rather than forcing rigid structure. Easier parsing for downstream systems.

---

### 5. **Streamlined Per-Criterion Format**

**Before (Lines 112-155):** 43 lines of format instructions per criterion including:
- Separate THOUGHT section
- Separate ACTION section with detailed evidence formatting
- Separate Counter-Evidence section
- Separate OBSERVATION section with 6 sub-categories
- Separate REFLECTION section
- Separate PRE-EMPTIVE DEFENSE section with 3 sub-items

**After:** 19 lines per criterion:
- Combined "What This Criterion Requires" (thought)
- Supporting Evidence (simple bullets)
- Counter-Evidence (simple bullets)
- Score + Confidence on one line
- Reasoning (2-3 sentences)
- Vulnerable Point (defense prep)

**Impact:** ~55% reduction in per-criterion format complexity. Still rigorous but more readable and faster to process.

---

### 6. **Reorganized Calibration Section**

**Before (Lines 200-218):**
- "EVALUATION QUALITY SELF-CHECK" with 4 subsections
- Multiple rhetorical questions
- Separate "Pattern Check" with sub-bullets

**After:**
- "CALIBRATION CHECK" with focused questions
- Combined into single flow
- Direct "My Honest Assessment" prompt

**Impact:** More actionable self-check that guides agent to final assessment rather than over-analyzing.

---

## What Was Preserved

✅ **ReAct framework** - Still follows Reasoning + Acting cycle
✅ **Evidence rigor** - Still requires both supporting AND counter-evidence
✅ **Level-aware evaluation** - Still distinguishes Current vs Target Level
✅ **Pre-emptive defense** - Still prepares for challenge agent
✅ **Rubric-first approach** - Still emphasizes letting rubric define criteria
✅ **Confidence tracking** - Still requires High/Medium/Low confidence per score
✅ **Self-calibration** - Still includes quality checks

---

## Expected Outcomes

1. **Faster evaluation** - ~40% reduction in output length means faster generation
2. **Better rubric compatibility** - Handles simple markdown rubrics without forcing weighted calculations
3. **More balanced evaluation** - Won't over-index on "we" vs "I" language
4. **Easier downstream parsing** - Simpler format is easier to extract scores/evidence from
5. **Maintained rigor** - All essential evaluation components preserved

---

## Migration Path

**Option 1: Direct Replacement**
Replace the current prompt with the improved version in `data/prompts/versions.json`:
```python
{
  "agent_name": "primary_agent",
  "version": 2,
  "content": "[paste improved prompt]",
  "created_at": "2026-01-08"
}
```

**Option 2: A/B Test**
Keep both versions and compare output quality across several test cases before switching.

**Option 3: Gradual Migration**
Implement changes in phases:
1. Phase 1: Fix weighted scoring assumption
2. Phase 2: Reduce output verbosity
3. Phase 3: Simplify format requirements

---

## Files

- **Original:** `primary_agent_prompt.txt` (9,243 characters, 264 lines)
- **Improved:** `primary_agent_prompt_improved.txt` (7,131 characters, 219 lines)
- **Reduction:** ~23% shorter prompt, estimated ~40% shorter output

---

## Next Steps

1. Review improved prompt with the team
2. Test with existing rubrics and transcripts
3. Compare output quality between versions
4. Update `data/prompts/versions.json` if approved
5. Consider similar improvements for challenge_agent and decision_agent prompts
