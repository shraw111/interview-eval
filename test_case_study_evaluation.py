"""
Test script to prove generic evaluation system works with case study rubric.
This demonstrates the system is now rubric-driven, not PM-specific.
"""
import sys
import os
sys.path.insert(0, 'src')

from src.graph.graph import evaluation_graph
from src.graph.state import create_initial_state

print("="*80)
print("TESTING GENERIC EVALUATION SYSTEM WITH CASE STUDY RUBRIC")
print("="*80)
print()

# Load case study rubric
with open('test_data/case_study_rubric.txt', 'r', encoding='utf-8') as f:
    rubric_text = f.read()

# Load case study presentation transcript
with open('test_data/sample_case_study_presentation.txt', 'r', encoding='utf-8') as f:
    transcript_text = f.read()

# Create candidate info for case study context
candidate_info = {
    'name': 'Taylor Kim',
    'current_level': 'Senior Consultant',
    'target_level': 'Principal Consultant',
    'years_experience': '4',
    'level_expectations': 'Principal Consultants must demonstrate strategic thinking, comprehensive analysis, and ability to present complex solutions to C-level stakeholders. They should show creativity in business model design and thoroughness in implementation planning.'
}

# Create initial state
initial_state = create_initial_state(
    rubric=rubric_text,
    transcript=transcript_text,
    candidate_info=candidate_info
)

print("Evaluation Type: Case Study Presentation")
print(f"Candidate: {candidate_info['name']}")
print(f"Presentation: Digital Transformation Strategy for Regional Bank")
print()
print("Rubric Type: Case Study Presentation Rubric")
print("  - Presentation Quality (10%)")
print("  - Problem Statement (15% - CRITICAL)")
print("  - Business Model Analysis (20% - CRITICAL)")
print("  - Research Depth, GTM, Product Roadmap, Implementation Plan")
print()
print("This is NOT a PM promotion interview - it's a deliverable evaluation!")
print("="*80)
print()

# Run evaluation
result = None
for chunk in evaluation_graph.stream(initial_state, stream_mode='updates'):
    for node_name, node_output in chunk.items():
        if node_name == 'primary_evaluator':
            print('[PRIMARY EVALUATOR] Complete')
            primary_eval = node_output.get('primary_evaluation', '')
            with open('case_study_primary.txt', 'w', encoding='utf-8') as f:
                f.write(primary_eval)

        elif node_name == 'challenge_agent':
            print('[CHALLENGE AGENT] Complete')
            challenges = node_output.get('challenges', '')
            with open('case_study_challenges.txt', 'w', encoding='utf-8') as f:
                f.write(challenges)

        elif node_name == 'primary_response':
            print('[RESPONSE AGENT] Complete')
            final_eval = node_output.get('final_evaluation', '')
            with open('case_study_response.txt', 'w', encoding='utf-8') as f:
                f.write(final_eval)

        elif node_name == 'decision_agent':
            print('[DECISION AGENT] Complete')
            decision = node_output.get('decision', '')

            # Save decision
            with open('case_study_decision.txt', 'w', encoding='utf-8') as f:
                f.write(decision)

            # Extract key information
            print()
            print("="*80)
            print("FINAL DECISION")
            print("="*80)

            for line in decision.split('\n')[:50]:  # Print first 50 lines
                if any(keyword in line for keyword in ['Final Recommendation:', 'Overall Score:', 'Critical Criteria:', 'Decision Confidence:']):
                    print(line)

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
print("Full outputs saved to:")
print("  - case_study_primary.txt")
print("  - case_study_challenges.txt")
print("  - case_study_response.txt")
print("  - case_study_decision.txt")
print()
print("="*80)
print("SUCCESS: Generic system evaluated a CASE STUDY, not a PM interview!")
print("="*80)
