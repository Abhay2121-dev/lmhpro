"""
ai_service.py  –  Gentle Reflection Prototype
Gemini API calls: reflection, continuation, risk classification, session summary.
All functions return plain dicts; errors are caught and returned gracefully.
"""
import json
import re
from typing import Optional

import streamlit as st
from google import genai
from google.genai import types

from prompts import COMPANION_SYSTEM, THEME_TAGS
from safety import Risk

MODEL = "gemma-4-26b-a4b-it"

# ── Client (cached so it survives Streamlit reruns) ──────────────────
@st.cache_resource
def _get_client(api_key: str) -> genai.Client:
    """Create and cache a Gemini client. One instance per API key."""
    return genai.Client(api_key=api_key)


def _client() -> genai.Client:
    key = st.secrets.get("GOOGLE_API_KEY", "")
    if not key or key == "your_google_api_key_here":
        raise ValueError("Add GOOGLE_API_KEY to .streamlit/secrets.toml")
    return _get_client(key)


def _call(prompt: str, system: Optional[str] = None, max_tokens: int = 1500) -> str:
    cfg = types.GenerateContentConfig(
        temperature=0.75,
        max_output_tokens=max_tokens,
        **({"system_instruction": system} if system else {}),
    )
    return _client().models.generate_content(
        model=MODEL, contents=prompt, config=cfg
    ).text


def _parse(raw: str) -> Optional[dict]:
    txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.MULTILINE)
    try:
        return json.loads(txt)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", txt, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except Exception:
                pass
    return None


# ── Gemini-based risk classification ──────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def classify_risk(text: str) -> Risk:
    prompt = f"""
Classify the risk in this grief journal entry. Look for suicidal ideation, 
self-harm intent, or hopelessness. Reply ONLY with valid JSON:
{{"risk_level": "<low|elevated|high>"}}

ENTRY:
\"\"\"{text}\"\"\"
"""
    try:
        raw = _call(prompt, system="Safety classifier. Respond only with requested JSON.")
        d = _parse(raw)
        if d:
            lvl = d.get("risk_level", "low").lower()
            if lvl in ("high", "elevated", "low"):
                return Risk(lvl)
    except Exception:
        pass
    return Risk.LOW


# ── Reflection ─────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def reflect(text: str, prompt_used: str, mode: str) -> dict:
    gp = f"""
You are a calm grief-journaling companion. Read this entry carefully.

MODE: {mode}
PROMPT: "{prompt_used}"
ENTRY:
\"\"\"{text}\"\"\"

Reply ONLY with valid JSON:
{{
  "reflection": "<2-4 warm, specific sentences reflecting the user's words. No diagnosis. No speaking for deceased.>",
  "follow_up_questions": ["<q1>", "<q2>", "<q3>"],
  "reminiscence_prompt": "<one gentle memory invitation>",
  "reframe": "<one compassionate reframe if guilt/shame appears, else empty string>",
  "continuation_starters": ["<s1>", "<s2>", "<s3>"],
  "theme_tags": ["<tag1>", "<tag2>", "<tag3>"],
  "session_summary": "<1-2 calm sentences summarising emotional territory covered>"
}}

theme_tags must be chosen only from: {THEME_TAGS}
Return ONLY valid JSON. No markdown.
"""
    try:
        raw = _call(gp, system=COMPANION_SYSTEM)
        d = _parse(raw)
        if d:
            return {
                "reflection": d.get("reflection", ""),
                "follow_up_questions": d.get("follow_up_questions", []),
                "reminiscence_prompt": d.get("reminiscence_prompt", ""),
                "reframe": d.get("reframe", ""),
                "continuation_starters": d.get("continuation_starters", []),
                "theme_tags": d.get("theme_tags", []),
                "session_summary": d.get("session_summary", ""),
                "error": None,
            }
    except Exception as e:
        return {**_empty(), "error": str(e)}
    return {**_empty(), "error": "Could not parse AI response."}


# ── Continuation starters ──────────────────────────────────────────────
def continue_writing(text: str, prompt_used: str) -> list[str]:
    gp = f"""
You are a calm grief-journaling companion.
PROMPT: "{prompt_used}"
ENTRY SO FAR:
\"\"\"{text}\"\"\"

Give exactly 3 short continuation starter phrases, warm and specific to what was written.
Reply ONLY with valid JSON:
{{"starters": ["<s1>", "<s2>", "<s3>"]}}
"""
    try:
        raw = _call(gp, system=COMPANION_SYSTEM, max_tokens=300)
        d = _parse(raw)
        if d and isinstance(d.get("starters"), list):
            return d["starters"][:3]
    except Exception:
        pass
    return [
        "What I remember most clearly is…",
        "Something I haven't said yet is…",
        "When I think about that time, I feel…",
    ]


# ── Session summary ────────────────────────────────────────────────────
def session_summary(entries: list[dict]) -> str:
    if not entries:
        return ""
    combined = "\n\n---\n\n".join(
        f"PROMPT: {e.get('prompt','')}\nENTRY: {e.get('text','')}"
        for e in entries
    )
    gp = f"""
You are a calm grief-journaling companion reviewing a full session.
SESSION:
\"\"\"{combined}\"\"\"

Write a brief, warm, affirming summary of the emotional territory covered today.
2-3 sentences max. No diagnosis. No speaking for the deceased.
Reply ONLY with valid JSON: {{"summary": "<text>"}}
"""
    try:
        raw = _call(gp, system=COMPANION_SYSTEM, max_tokens=300)
        d = _parse(raw)
        if d:
            return d.get("summary", "")
    except Exception:
        pass
    return ""


def _empty() -> dict:
    return {
        "reflection": "", "follow_up_questions": [],
        "reminiscence_prompt": "", "reframe": "",
        "continuation_starters": [], "theme_tags": [],
        "session_summary": "", "error": None,
    }
