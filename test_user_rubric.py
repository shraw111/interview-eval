"""
Test script using USER'S ACTUAL case study rubric.
"""
import sys
import os
sys.path.insert(0, 'src')

from src.graph.graph import evaluation_graph
from src.graph.state import create_initial_state

print("="*80)
print("TESTING WITH USER'S ACTUAL CASE STUDY RUBRIC")
print("="*80)
print()

# Load USER'S case study rubric
with open('test_data/user_case_study_rubric.txt', 'r', encoding='utf-8') as f:
    rubric_text = f.read()

# Load case study presentation transcript
with open('test_data/sample_case_study_presentation.txt', 'r', encoding='utf-8') as f:
    transcript_text = f.read()

# Create candidate info
candidate_info = {
    'name': 'Taylor Kim',
    'current_level': 'Senior Consultant',
    'target_level': 'Principal Consultant',
    'years_experience': '4',
    'level_expectations': 'Principal Consultants must demonstrate strategic thinking, comprehensive analysis, and ability to present complex solutions to C-level stakeholders.'
}

# Create initial state
initial_state = create_initial_state(
    rubric=rubric_text,
    transcript=transcript_text,
    candidate_info=candidate_info
)

print("Rubric Criteria (from user's actual rubric):")
print("  1. Presentation Quality (10%)")
print("  2. Presentation Structure (10%)")
print("  3. Story Telling Skills (10%)")
print("  4. Case Study Solution (60% total):")
print("     4a. Problem Statement (5%) - CRITICAL")
print("     4b. Opportunity Sizing (10%)")
print("     4c. Depth of Research (10%)")
print("     4d. Current Business Model (10%)")
print("     4e. Business Model Analysis (5%)")
print("     4f. Target Business Model Alternatives (10%) - CRITICAL")
print("     4g. Selection Framework (5%)")
print("     4h. GTM Approach (5%)")
print("     4i. Product Vision & Roadmap (5%)")
print("     4j. Implementation Plan (5%)")
print("  5. Others (10%)")
print()
print("="*80)
print()

# Run evaluation
print("Running evaluation...")
result = None
for chunk in evaluation_graph.stream(initial_state, stream_mode='updates'):
    for node_name, node_output in chunk.items():
        if node_name == 'primary_evaluator':
            print('[PRIMARY EVALUATOR] Complete')
            primary_eval = node_output.get('primary_evaluation', '')
            with open('user_rubric_primary.txt', 'w', encoding='utf-8') as f:
                f.write(primary_eval)

        elif node_name == 'challenge_agent':
            print('[CHALLENGE AGENT] Complete')
            challenges = node_output.get('challenges', '')
            with open('user_rubric_challenges.txt', 'w', encoding='utf-8') as f:
                f.write(challenges)

        elif node_name == 'primary_response':
            print('[RESPONSE AGENT] Complete')
            final_eval = node_output.get('final_evaluation', '')
            with open('user_rubric_response.txt', 'w', encoding='utf-8') as f:
                f.write(final_eval)

        elif node_name == 'decision_agent':
            print('[DECISION AGENT] Complete')
            decision = node_output.get('decision', '')

            # Save decision
            with open('user_rubric_decision.txt', 'w', encoding='utf-8') as f:
                f.write(decision)

            # Extract key information
            print()
            print("="*80)
            print("FINAL DECISION")
            print("="*80)

            # Print key lines
            for line in decision.split('\n'):
                if any(keyword in line for keyword in [
                    'Final Recommendation:',
                    'Overall Score:',
                    'Critical Criteria:',
                    'Decision Confidence:',
                    'Candidate:',
                    'Evaluation Type:'
                ]):
                    print(line.strip())

            result = node_output

print()
print("="*80)
print("EVALUATION COMPLETE!")
print("="*80)

metadata = result.get('metadata', {})
print(f"Total Tokens: {metadata.get('tokens', {}).get('total', 'N/A'):,}")
print(f"Cost: ${metadata.get('cost_usd', 'N/A')}")
print(f"Time: {metadata.get('execution_time_seconds', 'N/A')}s")
print()
print("Full evaluation saved to:")
print("  - user_rubric_primary.txt")
print("  - user_rubric_challenges.txt")
print("  - user_rubric_response.txt")
print("  - user_rubric_decision.txt")
print()
print("="*80)
print("This used YOUR actual case study rubric format!")
print("="*80)
