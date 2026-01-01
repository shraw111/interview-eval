# Sample Test Data

This folder contains realistic sample data for testing the PM Promotion Evaluator.

## Files

- **`sample_transcript.txt`** - Full PM promotion interview transcript (~2,500 words)
- **`sample_rubric.txt`** - Natural language evaluation rubric with criteria, weights, and decision rules
- **`candidate_info.txt`** - Candidate details to copy into the form

## How to Test

1. **Start the application:**
   ```bash
   streamlit run app/streamlit_app.py
   ```
   Open http://localhost:8501

2. **Fill in the form:**
   - Copy values from `candidate_info.txt` into the candidate fields
   - Copy entire contents of `sample_rubric.txt` into "Evaluation Criteria" field
   - Copy entire contents of `sample_transcript.txt` into "Interview Transcript" field

3. **Run evaluation:**
   - Click "🚀 Run Evaluation" button
   - Wait ~2-3 minutes for completion
   - Watch progress through 4 stages: Primary → Challenge → Response → Decision

4. **Review results:**
   - Check the final decision (STRONG RECOMMEND / RECOMMEND / BORDERLINE / DO NOT RECOMMEND)
   - Review evaluation reasoning
   - Check token usage and cost

## Expected Outcome

Based on the sample data:
- **Candidate:** Sarah Chen is a strong PM candidate with good strategic examples
- **Expected Decision:** Likely RECOMMEND or STRONG RECOMMEND
- **Critical Criteria:** Should meet both (Strategic Vision + Stakeholder Management)
- **Cost:** ~$0.50-0.80 for full evaluation

## Troubleshooting

If you encounter errors:
1. Check that `.env` file has valid `ANTHROPIC_ENDPOINT` and `ANTHROPIC_API_KEY`
2. Verify Streamlit is running (should see "You can now view your Streamlit app in your browser")
3. Check browser console for JavaScript errors
4. Review terminal output for Python errors

Report any errors and I'll fix them immediately.
