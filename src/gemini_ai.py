"""
Thin wrapper around the Gemini API used for AI-generated insights and the
natural-language assistant.

Uses the current `google-genai` SDK. The original project depended on
`google-generativeai`, which Google fully deprecated (support ended
30 Nov 2025) in favor of this unified client-based SDK.

This module also never raises at import time when no API key is
configured — it fails lazily, only when get_response() is actually
called. That way pages that don't need Gemini (or a fresh clone without
a .env yet) still load normally, and callers can check is_available()
to decide whether to show Gemini-powered features at all.
"""
from pathlib import Path
from dotenv import load_dotenv
from google import genai
import os

root = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=root / ".env")

GEMINI_ENABLED = os.getenv("GEMINI_ENABLED", "true").strip().lower() not in (
    "0",
    "false",
    "no",
    "off",
)
API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

_client = None


def is_available() -> bool:
    """Whether Gemini is enabled and a key is configured."""
    return GEMINI_ENABLED and bool(API_KEY)


def _get_client() -> genai.Client:
    global _client
    if not GEMINI_ENABLED:
        raise RuntimeError(
            "Gemini integration is disabled. Set GEMINI_ENABLED=true in your .env to enable it."
        )
    if not API_KEY:
        raise RuntimeError(
            "No Gemini API key found. Set GOOGLE_API_KEY or GEMINI_API_KEY in your .env file."
        )
    if _client is None:
        _client = genai.Client(api_key=API_KEY)
    return _client


def get_response(prompt: str) -> str:
    client = _get_client()
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        return response.text
    except Exception as e:
        message = str(e)
        if "403" in message or "denied" in message.lower():
            raise RuntimeError(
                "Gemini project access denied. Check your project permissions and API access."
            ) from e
        raise RuntimeError(f"Gemini API request failed: {message}") from e
