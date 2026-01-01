"""
History browser component using session state.
"""

import streamlit as st
from datetime import datetime


def render_history():
    """Render evaluation history from session state."""

    st.markdown("### 📊 Evaluation History")
    st.info("💾 History is stored in session and will be lost when you close the browser")

    history = st.session_state.get('evaluation_history', [])

    if not history:
        st.info("No evaluations yet. Run your first evaluation in the 'New Evaluation' tab!")
        return

    # Stats
    st.markdown(f"**Total Evaluations:** {len(history)}")

    st.markdown("---")

    # List evaluations
    for idx, eval_data in enumerate(history):
        candidate_name = eval_data.get('candidate_name', 'Unknown')
        timestamp = eval_data.get('timestamp', '')
        result = eval_data.get('result', {})
        metadata = result.get('metadata', {})

        # Format timestamp
        try:
            dt = datetime.fromisoformat(timestamp)
            date_str = dt.strftime("%b %d, %Y %H:%M")
        except:
            date_str = timestamp[:19] if timestamp else "Unknown"

        # Extract decision
        decision_text = result.get('decision', '')
        if "STRONG RECOMMEND" in decision_text.upper():
            decision_badge = "🟢 STRONG RECOMMEND"
        elif "DO NOT RECOMMEND" in decision_text.upper():
            decision_badge = "🔴 DO NOT RECOMMEND"
        elif "BORDERLINE" in decision_text.upper():
            decision_badge = "🟡 BORDERLINE"
        elif "RECOMMEND" in decision_text.upper():
            decision_badge = "🔵 RECOMMEND"
        else:
            decision_badge = "❓ Unknown"

        with st.expander(f"📄 {candidate_name} - {date_str} | {decision_badge}"):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Execution Time", f"{metadata.get('execution_time_seconds', 0):.0f}s")
            with col2:
                st.metric("Tokens", f"{metadata.get('tokens', {}).get('total', 0):,}")
            with col3:
                st.metric("Cost", f"${metadata.get('cost_usd', 0):.2f}")

            st.markdown("---")

            # Show decision highlight
            st.markdown("#### Final Decision")
            st.markdown(result.get('decision', 'N/A'))

            st.markdown("---")

            # Actions
            col_a, col_b, col_c = st.columns(3)

            with col_a:
                final_report = f"""# Evaluation Report

**Candidate:** {candidate_name}
**Date:** {date_str}

## Decision

{result.get('decision', 'N/A')}

## Calibrated Evaluation

{result.get('final_evaluation', 'N/A')}
"""
                st.download_button(
                    "📥 Download",
                    data=final_report,
                    file_name=f"{candidate_name}_evaluation.md",
                    mime="text/markdown",
                    key=f"download_{idx}",
                    use_container_width=True
                )

            with col_b:
                if st.button("👁️ View Full", key=f"view_{idx}", use_container_width=True):
                    st.session_state.evaluation_result = result
                    st.success("✓ Loaded to Results view - switch to 'New Evaluation' tab")

            with col_c:
                if st.button("🗑️ Delete", key=f"delete_{idx}", use_container_width=True):
                    st.session_state.evaluation_history.pop(idx)
                    st.rerun()
