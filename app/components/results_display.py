"""
Results display component showing 4-step evaluation journey.
"""

import streamlit as st
from typing import Dict, Any


def render_results(result: Dict[str, Any]):
    """Render evaluation results with 4-step journey."""

    st.markdown("---")
    st.markdown("## 📊 Final Evaluation Results")

    # Extract metadata
    metadata = result.get('metadata', {})

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Execution Time",
            f"{metadata.get('execution_time_seconds', 0):.0f}s"
        )

    with col2:
        st.metric(
            "Total Tokens",
            f"{metadata.get('tokens', {}).get('total', 0):,}"
        )

    with col3:
        st.metric(
            "Cost",
            f"${metadata.get('cost_usd', 0):.2f}"
        )

    with col4:
        st.metric(
            "Model",
            metadata.get('model_version', 'Unknown')[:20]
        )

    st.markdown("---")

    # 4-Step evaluation journey
    st.markdown("### 📊 Evaluation Journey")
    st.markdown("Primary → Challenge → Response → **Decision**")

    # Expandable sections for each step
    with st.expander("1️⃣ Initial Evaluation (Primary Agent)", expanded=False):
        st.markdown(result.get('primary_evaluation', 'N/A'))

    with st.expander("2️⃣ Challenges Raised (Challenge Agent)", expanded=False):
        st.markdown(result.get('challenges', 'N/A'))

    with st.expander("3️⃣ Calibrated Evaluation (Primary Response)", expanded=False):
        st.markdown(result.get('final_evaluation', 'N/A'))

    with st.expander("4️⃣ **Final Decision (Decision Agent)**", expanded=True):
        # Highlight the decision
        decision_text = result.get('decision', 'N/A')

        # Try to extract the recommendation from decision text
        if "STRONG RECOMMEND" in decision_text.upper():
            st.success("✅ **Recommendation: STRONG RECOMMEND**")
        elif "DO NOT RECOMMEND" in decision_text.upper():
            st.error("❌ **Recommendation: DO NOT RECOMMEND**")
        elif "BORDERLINE" in decision_text.upper():
            st.warning("⚠️ **Recommendation: BORDERLINE**")
        elif "RECOMMEND" in decision_text.upper():
            st.info("✓ **Recommendation: RECOMMEND**")

        st.markdown(decision_text)

    st.markdown("---")

    # Action buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        # Download final report
        final_report = f"""# Promotion Evaluation Report

**Candidate:** {result.get('candidate_info', {}).get('name', 'Unknown')}
**Current Level:** {result.get('candidate_info', {}).get('current_level', 'Unknown')}
**Target Level:** {result.get('candidate_info', {}).get('target_level', 'Unknown')}

---

## Final Decision

{result.get('decision', 'N/A')}

---

## Calibrated Evaluation

{result.get('final_evaluation', 'N/A')}

---

## Metadata

- **Execution Time:** {metadata.get('execution_time_seconds', 0):.1f}s
- **Total Tokens:** {metadata.get('tokens', {}).get('total', 0):,}
- **Cost:** ${metadata.get('cost_usd', 0):.2f}
- **Model:** {metadata.get('model_version', 'Unknown')}
"""
        st.download_button(
            label="📥 Download Full Report",
            data=final_report,
            file_name=f"evaluation_{result.get('candidate_info', {}).get('name', 'candidate').replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    with col2:
        if st.button("📊 View Token Breakdown", use_container_width=True):
            st.session_state.show_token_breakdown = not st.session_state.get('show_token_breakdown', False)

    with col3:
        if st.button("🔄 New Evaluation", use_container_width=True):
            # Clear evaluation result
            st.session_state.evaluation_result = None
            # Clear rubric approval to start fresh
            if 'rubric_approved' in st.session_state:
                del st.session_state.rubric_approved
            if 'structured_rubric' in st.session_state:
                del st.session_state.structured_rubric
            st.rerun()

    # Token breakdown (if requested)
    if st.session_state.get('show_token_breakdown', False):
        st.markdown("### 📊 Token Usage Breakdown")

        tokens = metadata.get('tokens', {})
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Primary Agent**")
            st.caption(f"Input: {tokens.get('primary_input', 0):,}")
            st.caption(f"Output: {tokens.get('primary_output', 0):,}")
            st.caption(f"**Total: {tokens.get('primary_input', 0) + tokens.get('primary_output', 0):,}**")

        with col2:
            st.markdown("**Challenge Agent**")
            st.caption(f"Input: {tokens.get('challenge_input', 0):,}")
            st.caption(f"Output: {tokens.get('challenge_output', 0):,}")
            st.caption(f"**Total: {tokens.get('challenge_input', 0) + tokens.get('challenge_output', 0):,}**")

        with col3:
            st.markdown("**Response Agent**")
            st.caption(f"Input: {tokens.get('final_input', 0):,}")
            st.caption(f"Output: {tokens.get('final_output', 0):,}")
            st.caption(f"**Total: {tokens.get('final_input', 0) + tokens.get('final_output', 0):,}**")

        st.markdown("**Decision Agent**")
        st.caption(f"Input: {tokens.get('decision_input', 0):,} | Output: {tokens.get('decision_output', 0):,} | Total: {tokens.get('decision_input', 0) + tokens.get('decision_output', 0):,}")

        st.markdown(f"**Grand Total: {tokens.get('total', 0):,} tokens**")
