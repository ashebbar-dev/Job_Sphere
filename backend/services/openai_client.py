import json
import os

import requests


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")


class OpenAIClientError(Exception):
    """Raised when calling the OpenAI Responses API fails."""


def _require_api_key():
    if not OPENAI_API_KEY:
        raise OpenAIClientError("OPENAI_API_KEY is not configured.")


def call_responses_api(payload, timeout=180):
    """
    Call the OpenAI Responses API directly.

    Args:
        payload (dict): JSON payload to send.
        timeout (int): Request timeout in seconds.

    Returns:
        dict: Parsed JSON response from API.
    """
    _require_api_key()
    url = f"{OPENAI_API_BASE.rstrip('/')}/responses"
    try:
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps(payload),
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise OpenAIClientError(f"OpenAI Responses API request failed: {exc}") from exc
