"""
safety.py  –  Gentle Reflection Prototype
Rule-based risk detection for journal entries.
"""
import re
from enum import Enum


class Risk(str, Enum):
    LOW = "low"
    ELEVATED = "elevated"
    HIGH = "high"


_HIGH = [
    r"\bsuicid\w*", r"\bkill\s+myself\b", r"\bend\s+(my\s+)?life\b",
    r"\bwant\s+to\s+die\b", r"\bhurt\s+myself\b", r"\bself[\s\-]harm\b",
    r"\bno\s+reason\s+to\s+(live|stay|go on)\b",
    r"\beveryone\s+would\s+be\s+better\s+off\s+without\s+me\b",
    r"\bI\s+should\s+not\s+be\s+here\b",
    r"\bdon'?t\s+want\s+to\s+be\s+here\b",
    r"\bcan'?t\s+go\s+on\b", r"\bnot\s+worth\s+living\b",
    # Planning / means
    r"\bhave\s+a\s+(plan|method|way)\s+to\b",
    r"\bgiving\s+(away|up)\s+(my\s+)?belongings\b",
    r"\bsaying\s+goodbye\b",
    r"\bwritten\s+(a\s+)?note\b",
    r"\blethal\b",
    r"\boverdose\b",
    r"\bend\s+it\s+(all|now)\b",
    r"\bno\s+way\s+out\b",
]
_ELEVATED = [
    r"\bfeeling\s+hopeless\b", r"\bno\s+hope\b",
    r"\bburden\s+to\b", r"\bwish\s+I\s+could\s+disappear\b",
    r"\bwish\s+I\s+hadn'?t\s+woken\b", r"\bgive\s+up\b",
    r"\bdon'?t\s+see\s+(any\s+)?point\b",
    # Additional elevated indicators
    r"\bnothing\s+(to\s+live|left)\b",
    r"\btired\s+of\s+(living|being\s+alive)\b",
    r"\bwould\s+be\s+better\s+off\s+dead\b",
    r"\bdon'?t\s+care\s+(if\s+I|whether\s+I)\s+(live|die)\b",
    r"\bwish\s+it\s+was\s+over\b",
    r"\bcan'?t\s+take\s+(this|it)\s+anymore\b",
]

CRISIS_MSG = """
What was described may indicate serious distress.

This system cannot provide crisis support.

It is important to contact a qualified professional or a trusted person.

If you are in immediate danger, contact local emergency services.

---
**Crisis resources (US):**
- 988 Suicide & Crisis Lifeline — Call or text **988**
- Crisis Text Line — Text **HOME** to **741741**
- Emergency services — Call **911**
"""

ELEVATED_MSG = (
    "If support is needed, contact a qualified professional or a trusted person. "
    "The 988 Suicide & Crisis Lifeline is available at any time — call or text **988**."
)

# Displayed at ELEVATED risk level below the 988 banner.
# Offers neutral writing directions. No empathy, no advice, no social language.
SUICIDALITY_ADJACENT_MSG = (
    "Writing can continue in any direction. The following topics are available "
    "if any are relevant:"
)


def check(text: str) -> Risk:
    t = text.lower()
    for p in _HIGH:
        if re.search(p, t, re.I):
            return Risk.HIGH
    for p in _ELEVATED:
        if re.search(p, t, re.I):
            return Risk.ELEVATED
    return Risk.LOW
