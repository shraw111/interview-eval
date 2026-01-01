"""
Prompt editor component for managing 4 agent prompts.
"""

import streamlit as st
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from src.prompts.manager import PromptManager


def render_prompt_editor():
    """Render prompt editing interface for 4 agents."""

    st.markdown("### 📚 Prompt Management")
    st.info("⚠️ Editing prompts affects all future evaluations")

    pm = PromptManager()

    col1, col2 = st.columns([1, 3])

    with col1:
        st.markdown("#### Select Prompt")

        prompt_type_display = st.radio(
            "Agent",
            ["Rubric Structuring", "Primary Evaluator", "Challenge Reviewer", "Decision Maker"],
            key="selected_prompt_type"
        )

        # Map display names to keys
        prompt_type_map = {
            "Rubric Structuring": "rubric_structuring_agent",
            "Primary Evaluator": "primary_agent",
            "Challenge Reviewer": "challenge_agent",
            "Decision Maker": "decision_agent"
        }
        prompt_key = prompt_type_map[prompt_type_display]

        st.markdown("---")
        st.markdown("#### Version History")

        versions = pm.get_all_versions(prompt_key)
        active_version = pm._load_versions()[prompt_key]["active_version"]

        for version_data in reversed(versions):
            version = version_data["version"]
            is_active = version == active_version

            label = f"v{version} {'✓ Active' if is_active else ''}"

            if st.button(label, key=f"version_{prompt_key}_{version}", use_container_width=True):
                st.session_state.selected_version = version
                st.session_state.selected_prompt_key = prompt_key

        st.markdown("---")

        if st.button("➕ Create New Version", use_container_width=True):
            st.session_state.creating_new = True
            st.session_state.selected_prompt_key = prompt_key

    with col2:
        # Determine what to show
        if 'selected_version' in st.session_state and st.session_state.get('selected_prompt_key') == prompt_key:
            selected = st.session_state.selected_version
            version_data = pm.get_version(prompt_key, selected)
        else:
            # Show active version
            active_version = pm._load_versions()[prompt_key]["active_version"]
            version_data = pm.get_version(prompt_key, active_version)

        st.markdown(f"#### Editing: {prompt_type_display} - v{version_data['version']}")

        # Show metadata
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            st.caption(f"Created: {version_data['created_at'][:10]}")
        with col2_2:
            st.caption(f"Notes: {version_data['notes']}")

        # Prompt editor
        prompt_content = st.text_area(
            "Prompt Content",
            value=version_data['content'],
            height=400,
            key=f"prompt_editor_{prompt_key}"
        )

        st.caption(f"Character count: {len(prompt_content):,}")

        # Actions
        col2_1, col2_2, col2_3 = st.columns(3)

        with col2_1:
            if st.button("💾 Save as New Version", use_container_width=True):
                st.session_state.show_save_dialog = True
                st.session_state.current_prompt_content = prompt_content

        with col2_2:
            if st.button("🔄 Set as Active", use_container_width=True):
                try:
                    pm.set_active_version(prompt_key, version_data['version'])
                    st.success(f"✓ v{version_data['version']} is now active")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        with col2_3:
            if st.button("↩️ Revert Changes", use_container_width=True):
                st.rerun()

        # Save dialog
        if st.session_state.get('show_save_dialog', False):
            with st.form("save_version_form"):
                st.markdown("#### Save New Version")

                version_notes = st.text_input(
                    "Version Notes*",
                    placeholder="What changed in this version?"
                )

                set_active = st.checkbox("Set as active version")

                col_submit, col_cancel = st.columns(2)

                with col_submit:
                    submitted = st.form_submit_button("💾 Save", use_container_width=True)

                    if submitted:
                        if not version_notes:
                            st.error("Version notes are required")
                        else:
                            try:
                                new_version = pm.save_new_version(
                                    prompt_type=prompt_key,
                                    content=st.session_state.current_prompt_content,
                                    notes=version_notes,
                                    set_active=set_active
                                )

                                st.success(f"✓ Saved as v{new_version}")
                                st.session_state.show_save_dialog = False
                                if 'current_prompt_content' in st.session_state:
                                    del st.session_state.current_prompt_content
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error saving: {str(e)}")

                with col_cancel:
                    if st.form_submit_button("Cancel", use_container_width=True):
                        st.session_state.show_save_dialog = False
                        if 'current_prompt_content' in st.session_state:
                            del st.session_state.current_prompt_content
                        st.rerun()
