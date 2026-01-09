"""
Azure OpenAI client wrapper with retry logic and cost tracking.
"""

import os
import yaml
import time
import sys
from typing import Tuple
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def log_to_stderr(message: str):
    """Log to stderr to avoid console encoding issues."""
    try:
        sys.stderr.write(f"{message}\n")
        sys.stderr.flush()
    except:
        pass  # Silently fail if stderr also has encoding issues


# Load config
config_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "config.yaml"
)
with open(config_path, "r") as f:
    config = yaml.safe_load(f)


def get_azure_openai_client() -> AzureOpenAI:
    """
    Get configured Azure OpenAI client.

    Returns:
        Configured Azure OpenAI client instance
    """
    # Support both naming conventions
    api_key = os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("AZURE_OPENAI_KEY")

    return AzureOpenAI(
        api_key=api_key,
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        timeout=600.0  # 10 minute timeout for long transcripts
    )


def call_anthropic_claude(
    model_name: str,
    system_prompt: str,
    user_message: str,
    max_tokens: int,
    temperature: float = 0.0
) -> Tuple[str, int, int]:
    """
    Call Azure OpenAI with retry logic.

    Args:
        model_name: Deployment name (e.g., "gpt-4o")
        system_prompt: System prompt text
        user_message: User message text
        max_tokens: Maximum tokens to generate
        temperature: Temperature for sampling (default 0.0)

    Returns:
        Tuple of (response_text, input_tokens, output_tokens)

    Raises:
        Exception: If API call fails after all retries
    """
    client = get_azure_openai_client()
    # Support both naming conventions
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME") or os.getenv("AZURE_OPENAI_DEPLOYMENT")

    max_retries = config["retry"]["max_attempts"]
    backoff = config["retry"]["backoff_factor"]

    for attempt in range(max_retries):
        try:
            api_start = time.time()
            log_to_stderr(f"[API CALL START] Deployment: {deployment}, max_tokens: {max_tokens}, attempt: {attempt + 1}/{max_retries}")

            # Use max_completion_tokens for newer models (gpt-5.2-chat, etc.)
            # Some models like gpt-5.2-chat only support temperature=1, so omit if 0.0
            params = {
                "model": deployment,
                "max_completion_tokens": max_tokens,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            }

            # Only add temperature if not 0.0 (some models don't support it)
            if temperature != 0.0:
                params["temperature"] = temperature

            response = client.chat.completions.create(**params)

            api_duration = time.time() - api_start
            log_to_stderr(f"[API CALL SUCCESS] Duration: {api_duration:.2f}s")

            # Extract response text
            text = response.choices[0].message.content

            # Extract token counts
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

            log_to_stderr(f"[TOKENS] Input: {input_tokens:,}, Output: {output_tokens:,}")

            return text, input_tokens, output_tokens

        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = backoff ** attempt
                log_to_stderr(f"API error (attempt {attempt + 1}/{max_retries}), retrying in {wait_time}s: {str(e)[:100]}")
                time.sleep(wait_time)
            else:
                raise Exception(f"Azure OpenAI API call failed after {max_retries} attempts: {str(e)}")


def calculate_cost(input_tokens: int, output_tokens: int) -> float:
    """
    Calculate cost in USD based on token usage.

    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        Cost in USD
    """
    input_cost = input_tokens * config["pricing"]["input_cost_per_mtok"] / 1_000_000
    output_cost = output_tokens * config["pricing"]["output_cost_per_mtok"] / 1_000_000
    return input_cost + output_cost
