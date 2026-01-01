"""
Input form component for candidate info and transcript.
"""

import streamlit as st
from typing import Optional, Dict, Any


def render_input_form() -> Optional[Dict[str, Any]]:
    """
    Render input form for evaluation.

    Returns:
        Validated form data or None if incomplete
    """
    with st.form("evaluation_form"):
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("### 👤 Candidate Information")

            name = st.text_input("Name*", key="candidate_name")

            col1_1, col1_2 = st.columns(2)
            with col1_1:
                current_level = st.text_input("Current Level*", placeholder="e.g. PM", key="current_level")
            with col1_2:
                target_level = st.text_input("Target Level*", placeholder="e.g. Senior PM", key="target_level")

            years_exp = st.number_input(
                "Years at Current Level",
                min_value=0,
                max_value=50,
                value=3,
                key="years_exp"
            )

            level_expectations = st.text_area(
                "Level Expectations*",
                placeholder="What distinguishes Target from Current level?\n\nExample: Senior PMs define strategy vs execute on roadmap",
                height=100,
                key="level_expectations"
            )

            st.markdown("---")

            st.markdown("### 📋 Evaluation Rubric")
            rubric = st.text_area(
                "Evaluation Criteria* (Natural Language)",
                placeholder="""Describe your evaluation criteria in plain language. Example:

I need to evaluate a PM for promotion to Senior PM.

**Critical Criteria (must-haves):**
- Strategic thinking: Can they define 12-18 month product vision and influence company direction?
- Stakeholder management: Do they proactively align executives and drive consensus?

**Important Criteria:**
- Execution: Track record of delivering complex, multi-quarter initiatives
- Team leadership: Mentoring junior PMs and elevating team capabilities
- Data-driven decisions: Using metrics to validate assumptions

The candidate should demonstrate clear evidence of operating at Senior PM level, not just potential.""",
                height=300,
                key="rubric_text"
            )

            if rubric:
                st.caption(f"Characters: {len(rubric):,}")

        with col2:
            st.markdown("### 📄 Interview Transcript")

            transcript_option = st.radio(
                "Transcript Source",
                ["Paste Text", "Upload File"],
                key="transcript_option"
            )

            transcript = None
            if transcript_option == "Paste Text":
                transcript = st.text_area(
                    "Interview Transcript*",
                    height=500,
                    placeholder="Paste the complete interview transcript here...",
                    key="transcript_text"
                )

                if transcript:
                    char_count = len(transcript)
                    st.caption(f"Characters: {char_count:,}")
                    if char_count > 100000:
                        st.warning("Very long transcript - may take longer to process")

            else:  # Upload File
                uploaded_file = st.file_uploader(
                    "Upload Transcript (.txt, .md)",
                    type=['txt', 'md'],
                    key="transcript_file"
                )

                if uploaded_file:
                    transcript = uploaded_file.read().decode('utf-8')
                    st.success(f"Loaded: {len(transcript):,} characters")

        # Submit button
        submitted = st.form_submit_button("🚀 Run Evaluation", type="primary", use_container_width=True)

        # Validate and return
        if submitted:
            if all([name, current_level, target_level, level_expectations, rubric, transcript]):
                return {
                    'candidate_info': {
                        'name': name,
                        'current_level': current_level,
                        'target_level': target_level,
                        'years_experience': years_exp,
                        'level_expectations': level_expectations
                    },
                    'rubric': rubric,
                    'transcript': transcript
                }
            else:
                st.error("Please fill in all required fields (*)")
                return None

    return None
