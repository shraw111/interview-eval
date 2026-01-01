# PM Promotion Evaluator

Three-agent AI evaluation system for assessing PM promotion candidates using LangGraph and Anthropic Claude (via Azure Foundry).

## Features

- **3 Evaluation Agents**: Primary evaluator, Challenge reviewer, Decision maker
- **Natural Language Rubrics**: Write evaluation criteria in plain English - no structured format needed
- **ReAct Framework**: Rigorous evaluation with reasoning and evidence tracking
- **Anthropic Claude Integration**: Claude Sonnet 4.5 via Azure Foundry
- **Streamlit UI**: Clean interface for evaluation and results

## Architecture

```
User Input (Natural Language Rubric + Transcript)
  ↓
[Primary Agent] → Initial evaluation
  ↓
[Challenge Agent] → Peer review
  ↓
[Response Agent] → Calibrated evaluation
  ↓
[Decision Agent] → Final recommendation
```

## Setup

### 1. Prerequisites
- Python 3.11 or higher
- Anthropic Claude access via Azure Foundry endpoint

### 2. Install Dependencies
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Anthropic Claude
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Anthropic Foundry credentials:
# ANTHROPIC_ENDPOINT=https://your-resource.services.ai.azure.com/anthropic/
# ANTHROPIC_API_KEY=your_api_key_here
```

### 4. Configure Model Names
Edit `config.yaml` to specify model names (default is `claude-sonnet-4-5`):
```yaml
models:
  rubric_structuring_agent:
    model_name: "claude-sonnet-4-5"  # Or other available Claude model
  primary_agent:
    model_name: "claude-sonnet-4-5"
  # ... etc
```

### 5. Run Application
```bash
streamlit run app/streamlit_app.py
```

Open browser to http://localhost:8501

## Usage

### 1. Enter Candidate Info
- Name, current level, target level
- Years of experience
- Level expectations (what distinguishes target from current level)

### 2. Write Evaluation Rubric
- Describe your evaluation criteria in plain English
- Specify which criteria are critical (must-haves)
- No need to structure into YAML - the AI interprets natural language directly

### 3. Provide Transcript
- Paste interview transcript
- Or upload a .txt file

### 4. Run Evaluation
- Click "Run Evaluation"
- Wait ~2-3 minutes for 4-agent workflow
- Progress tracked: Primary (25%) → Challenge (50%) → Response (75%) → Decision (100%)

### 5. Review Results
- See complete evaluation journey
- Final promotion decision (Strong Recommend / Recommend / Borderline / Do Not Recommend)
- Download report as Markdown

## Editing Prompts

1. Go to "Prompts" tab
2. Select agent (Primary / Challenge / Decision)
3. Edit prompt text
4. Save as new version
5. Set as active to use in evaluations

## Cost Estimation

- Typical evaluation: ~35-45K tokens (3 agents: Primary, Challenge, Decision)
- Cost per evaluation: ~$0.50-0.80 (Claude Sonnet 4.5: $3/MTok input, $15/MTok output)
- No additional cost for rubric structuring - natural language passed directly

## Project Structure

```
interview-agent/
├── src/                # Core logic
│   ├── graph/          # LangGraph nodes & workflow
│   ├── prompts/        # Prompt management
│   └── utils/          # Anthropic Claude client
├── app/                # Streamlit UI
│   └── components/     # UI components
├── data/               # Prompts & sample data
│   ├── prompts/        # Agent prompt versions
│   └── rubrics/        # Sample rubrics
└── tests/              # Test fixtures
```

## Troubleshooting

**Anthropic Claude Errors:**
- Check `.env` file has correct Anthropic Foundry endpoint and API key
- Verify model names in `config.yaml` (default: claude-sonnet-4-5)
- Ensure endpoint URL ends with `/anthropic/`
- Restart Streamlit after editing `.env`

**Import Errors:**
- Ensure you're in the project directory
- Check virtual environment is activated

**Slow Evaluations:**
- Normal: 120-180 seconds for full 4-agent workflow
- Check internet connection
- Verify Anthropic Claude service via Azure Foundry is responsive

## License

MIT
