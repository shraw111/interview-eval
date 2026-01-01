"""
Main Streamlit application with Anthropic Claude (via Azure Foundry) integration.
"""

import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Page config
st.set_page_config(
    page_title="PM Promotion Evaluator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import components
from components.input_form import render_input_form
from components.prompt_editor import render_prompt_editor
from components.results_display import render_results
from components.history import render_history

# Import graph
from src.graph.graph import evaluation_graph
from src.graph.state import create_initial_state


# Initialize session state
if 'evaluation_result' not in st.session_state:
    st.session_state.evaluation_result = None

if 'evaluation_history' not in st.session_state:
    st.session_state.evaluation_history = []

if 'openai_configured' not in st.session_state:
    # Check Azure OpenAI configuration
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    st.session_state.openai_configured = bool(endpoint and api_key and deployment)


# Header
st.title("🎯 PM Promotion Evaluator")
st.markdown("Three-agent evaluation system with Azure OpenAI GPT-4o")

# Check Azure OpenAI configuration
if not st.session_state.openai_configured:
    st.error("⚠️ Azure OpenAI not configured")
    st.markdown("""
Please set up your Azure OpenAI credentials:

1. Copy `.env.example` to `.env`
2. Add your Azure OpenAI credentials:
   ```
   AZURE_OPENAI_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
   AZURE_OPENAI_KEY=your_api_key_here
   AZURE_OPENAI_DEPLOYMENT=gpt-4o
   AZURE_OPENAI_API_VERSION=2025-01-01-preview
   ```
3. Restart Streamlit: `streamlit run app/streamlit_app.py`
    """)
    st.stop()

# Tabs
tab1, tab2, tab3 = st.tabs(["📋 New Evaluation", "📚 Prompts", "📊 History"])

with tab1:
    # Render input form
    form_data = render_input_form()

    # Run evaluation if form was submitted
    if form_data:
        # Create initial state
        initial_state = create_initial_state(
            rubric=form_data['rubric'],
            transcript=form_data['transcript'],
            candidate_info=form_data['candidate_info']
        )

        # Run graph with 4-step progress tracking
        with st.spinner("Running evaluation... This takes ~2-3 minutes"):
            try:
                # Progress indicators
                progress_container = st.container()

                with progress_container:
                    st.markdown("### Evaluation Progress")
                    progress_bar = st.progress(0, text="Starting evaluation...")
                    log_container = st.container()

                    # Run graph
                    result = None
                    current_state = initial_state

                    import time
                    start_time = time.time()

                    for chunk in evaluation_graph.stream(initial_state, stream_mode="updates"):
                        # chunk is a dict with node_name as key
                        for node_name, node_output in chunk.items():
                            elapsed = time.time() - start_time

                            with log_container:
                                st.info(f"[{elapsed:.1f}s] Processing: {node_name}")

                            # Merge updates into current state
                            for key, value in node_output.items():
                                if key in current_state:
                                    if isinstance(value, dict) and isinstance(current_state[key], dict):
                                        # Merge dictionaries (for metadata)
                                        current_state[key] = {**current_state[key], **value}
                                    else:
                                        current_state[key] = value

                            # Update progress based on node
                            if node_name == "primary_evaluator":
                                progress_bar.progress(25, text="Primary evaluation complete (1/4)")

                                # Show token stats
                                metadata = node_output.get("metadata", {})
                                tokens = metadata.get("tokens", {})
                                with log_container:
                                    st.success(f"✓ Primary Agent: {tokens.get('primary_input', 0):,} input tokens → {tokens.get('primary_output', 0):,} output tokens")

                                with st.expander("Initial Evaluation", expanded=False):
                                    st.markdown(node_output.get("primary_evaluation", ""))

                            elif node_name == "challenge_agent":
                                progress_bar.progress(50, text="Challenge review complete (2/4)")

                                # Show token stats
                                metadata = node_output.get("metadata", {})
                                tokens = metadata.get("tokens", {})
                                with log_container:
                                    st.success(f"✓ Challenge Agent: {tokens.get('challenge_input', 0):,} input tokens → {tokens.get('challenge_output', 0):,} output tokens")

                                with st.expander("Challenges Raised", expanded=False):
                                    st.markdown(node_output.get("challenges", ""))

                            elif node_name == "primary_response":
                                progress_bar.progress(75, text="Calibrated evaluation complete (3/4)")

                                # Show token stats
                                metadata = node_output.get("metadata", {})
                                tokens = metadata.get("tokens", {})
                                with log_container:
                                    st.success(f"✓ Response Agent: {tokens.get('response_input', 0):,} input tokens → {tokens.get('response_output', 0):,} output tokens")

                                with st.expander("Calibrated Evaluation", expanded=False):
                                    st.markdown(node_output.get("final_evaluation", ""))

                            elif node_name == "decision_agent":
                                progress_bar.progress(100, text="Final decision made! (4/4)")

                                # Show token stats
                                metadata = node_output.get("metadata", {})
                                tokens = metadata.get("tokens", {})
                                with log_container:
                                    st.success(f"✓ Decision Agent: {tokens.get('decision_input', 0):,} input tokens → {tokens.get('decision_output', 0):,} output tokens")

                                result = current_state

                                with st.expander("Final Decision", expanded=True):
                                    st.markdown(node_output.get("decision", ""))

                    # Store result
                    st.session_state.evaluation_result = result

                    # Add to history
                    st.session_state.evaluation_history.insert(0, {
                        'candidate_name': form_data['candidate_info']['name'],
                        'timestamp': result['metadata']['timestamps']['decision'],
                        'result': result
                    })

                    st.success("Evaluation complete!")

            except Exception as e:
                st.error(f"Error during evaluation: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

    # Display results if available
    if st.session_state.evaluation_result:
        render_results(st.session_state.evaluation_result)

with tab2:
    render_prompt_editor()

with tab3:
    render_history()
