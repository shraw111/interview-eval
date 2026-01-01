"""
Quick test script to verify the evaluation workflow works end-to-end.
"""

from src.graph.graph import evaluation_graph
from src.graph.state import create_initial_state

# Sample data
candidate_info = {
    'name': 'Test Candidate',
    'current_level': 'PM',
    'target_level': 'Senior PM',
    'years_experience': 3,
    'level_expectations': 'Senior PMs should define strategy, not just execute. They should influence product direction and align stakeholders.'
}

rubric = """
I need to evaluate a PM for promotion to Senior PM.

**Critical Criteria:**
- Strategic thinking: Can they define product vision and influence direction?
- Stakeholder management: Do they proactively align executives?

**Important:**
- Execution: Track record of delivering complex initiatives
- Leadership: Mentoring and elevating team
"""

transcript = """
Interviewer: Tell me about a time you influenced product strategy.

Candidate: At my last company, I noticed our mobile app had poor retention. I analyzed user data and found that 60% of users churned after day 3. I proposed a complete onboarding redesign focused on time-to-value.

I brought together engineering, design, and data science to create a cross-functional team. We ran experiments and reduced time-to-first-value from 5 days to 1 day. This increased D30 retention from 25% to 45%.

Interviewer: How did you get buy-in from leadership?

Candidate: I created a one-pager showing the revenue impact - $2M ARR if we improved retention by 10 points. The CEO was skeptical, so I ran a small pilot with 5% of users first. When we saw positive results, I got approval for full rollout.
"""

# Create initial state
initial_state = create_initial_state(
    rubric=rubric,
    transcript=transcript,
    candidate_info=candidate_info
)

print("Starting evaluation test...")
print("=" * 60)

try:
    result = None
    for chunk in evaluation_graph.stream(initial_state, stream_mode="updates"):
        for node_name, node_output in chunk.items():
            print(f"\n[{node_name.upper()}]")

            if "primary_evaluation" in node_output:
                print(f"Primary evaluation: {len(node_output['primary_evaluation'])} chars")
            elif "challenges" in node_output:
                print(f"Challenges: {len(node_output['challenges'])} chars")
            elif "final_evaluation" in node_output:
                print(f"Final evaluation: {len(node_output['final_evaluation'])} chars")
            elif "decision" in node_output:
                print(f"Decision: {len(node_output['decision'])} chars")
                result = {**initial_state, **node_output}

    if result and result.get('decision'):
        print("\n" + "=" * 60)
        print("EVALUATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\nTokens used: {result['metadata']['tokens'].get('total', 'N/A')}")
        print(f"Cost: ${result['metadata'].get('cost_usd', 'N/A')}")
        print(f"Execution time: {result['metadata'].get('execution_time_seconds', 'N/A')}s")
        print("\n--- DECISION ---")
        print(result['decision'][:500] + "..." if len(result['decision']) > 500 else result['decision'])
    else:
        print("\nERROR: Evaluation did not complete - no decision received")

except Exception as e:
    print(f"\nERROR: {str(e)}")
    import traceback
    traceback.print_exc()
