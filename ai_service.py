"""
ai_service.py  –  Bereavement Writing Prototype
Gemini API calls: content observation, continuation, risk classification, session summary.
All functions return plain dicts; errors are caught and returned gracefully.
"""
import json
import os
import re
from typing import Optional

import streamlit as st
from google import genai
from google.genai import types

from prompts import COMPANION_SYSTEM, THEME_TAGS
from safety import Risk

MODEL = "gemini-2.5-flash-lite"
PLACEHOLDER_API_KEY = "your_google_api_key_here"
MISSING_API_KEY_MESSAGE = (
    "Missing GOOGLE_API_KEY. For local runs, add it to "
    "`.streamlit/secrets.toml`. For Streamlit Community Cloud, add "
    "`GOOGLE_API_KEY = \"...\"` in App settings -> Secrets, then restart the app."
)

# ── Client (cached so it survives Streamlit reruns) ──────────────────
@st.cache_resource
def _get_client(api_key: str) -> genai.Client:
    """Create and cache a Gemini client. One instance per API key."""
    return genai.Client(api_key=api_key)


def _configured_api_key() -> str:
    """Read the API key from Streamlit secrets first, then the environment."""
    try:
        key = st.secrets.get("GOOGLE_API_KEY", "")
    except Exception:
        key = ""
    if not key:
        key = os.getenv("GOOGLE_API_KEY", "")
    return key.strip()


def api_key_error() -> Optional[str]:
    key = _configured_api_key()
    if not key:
        return MISSING_API_KEY_MESSAGE
    if key == PLACEHOLDER_API_KEY:
        return "Replace the placeholder GOOGLE_API_KEY value with a real API key."
    return None


def is_configured() -> bool:
    return api_key_error() is None


def _client() -> genai.Client:
    error = api_key_error()
    if error:
        raise ValueError(error)
    return _get_client(_configured_api_key())


def _call(prompt: str, system: Optional[str] = None, max_tokens: int = 900) -> str:
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
# ── Reflection ─────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def reflect(text: str, prompt_used: str, mode: str) -> dict:
    gp = f"""
Read the following journal entry and respond ONLY with valid JSON.

MODE: {mode}
PROMPT: "{prompt_used}"
ENTRY:
\"\"\"{text}\"\"\"

Instructions:
- Describe what was written in neutral, content-focused terms.
- Do NOT use 'I', 'we', or any relational language.
- Do NOT express empathy, validation, reassurance, or emotional interpretation.
- Do NOT say 'It sounds like [emotion] is present', 'It is okay to feel this way', 'acknowledge it', or similar companion-style phrasing.
- Do NOT infer or label emotions (e.g., do not say 'you seem sad').
- Do NOT give advice, guidance, or therapeutic reframes.
- Use formal, non-emotional language throughout.

For follow_up_questions: generate 3 writing prompts that invite the writer to recall and describe something
specific and concrete — a particular memory, place, situation, object, time of day, or sensory detail
connected to what was written. Focus on WHERE things happened, WHAT was present in the environment,
WHAT triggered the feeling or thought, or WHICH specific moment they are thinking of.
Examples of the right style: "Where were you when this happened?", "What do you recall about that place?",
"What specific moment comes to mind?", "What did the surroundings look like at the time?",
"What triggered this memory today?", "What object or place is most connected to this?".
Keep all questions neutral, content-specific, and non-interpretive.

For continuation_starters: provide 3 short sentence-opening phrases that lead the writer toward
a specific memory, place, or situation (e.g. "The place I most associate with this is…",
"What I remember about that moment is…", "One thing that still brings this back is…").

Reply ONLY with valid JSON:
{{
  "reflection": "<1-3 neutral sentences describing what was written. Content-focused, not person-focused. No empathy, no 'I', no relational language.>",
  "follow_up_questions": ["<q about a specific memory, place, or situation>", "<q about a sensory detail or trigger>", "<q about a specific moment or circumstance>"],
  "reframe": "",
  "continuation_starters": ["<starter leading toward a specific memory or place>", "<starter leading toward a trigger or object>", "<starter leading toward a specific moment>"],
  "theme_tags": ["<tag1>", "<tag2>", "<tag3>"]
}}

theme_tags must be chosen only from: {THEME_TAGS}
Return ONLY valid JSON. No markdown.
"""
    try:
        raw = _call(gp, system=COMPANION_SYSTEM, max_tokens=550)
        d = _parse(raw)
        if d:
            return {
                "reflection": d.get("reflection", ""),
                "follow_up_questions": d.get("follow_up_questions", []),
                "reframe": d.get("reframe", ""),
                "continuation_starters": d.get("continuation_starters", []),
                "theme_tags": d.get("theme_tags", []),
                "error": None,
            }
    except Exception as e:
        return {**_empty(), "error": str(e)}
    return {**_empty(), "error": "Could not parse AI response."}


# ── Continuation starters ──────────────────────────────────────────────
def continue_writing(text: str, prompt_used: str) -> list[str]:
    gp = f"""
Read the following journal entry written in response to: "{prompt_used}".

ENTRY SO FAR:
\"\"\"{text}\"\"\"

Give exactly 3 short neutral continuation starter phrases that are specific to the written content.
Do NOT use empathetic or relational language. Do NOT include 'I feel' or emotional interpretation.
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
Review the following journal session entries and produce a brief neutral summary of the content areas and topics covered.

SESSION:
\"\"\"{combined}\"\"\"

Instructions:
- Describe the content structurally (e.g., topics, memories, events mentioned).
- Do NOT use empathy, validation, or emotional language.
- Do NOT use 'I', 'we', or relational language.
- 2-3 sentences maximum.
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
