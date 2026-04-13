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
]
_ELEVATED = [
    r"\bfeeling\s+hopeless\b", r"\bno\s+hope\b",
    r"\bburden\s+to\b", r"\bwish\s+I\s+could\s+disappear\b",
    r"\bwish\s+I\s+hadn'?t\s+woken\b", r"\bgive\s+up\b",
    r"\bdon'?t\s+see\s+(any\s+)?point\b",
]

CRISIS_MSG = """
## 🤍 You Are Not Alone

Something in what you've written suggests you may be going through an especially difficult moment.

**Please reach out:**
- **988 Suicide & Crisis Lifeline** → Call or text **988** (US, 24/7)
- **Crisis Text Line** → Text **HOME** to **741741**
- **Emergency services** → Call **911**

---
💬 *A message you can send right now:*
> "I'm having a really hard time and I need some support. Can we talk?"

---
*This journaling app is not a substitute for mental health care.*
"""

ELEVATED_MSG = (
    "🌿 *A gentle note:* If things feel overwhelming today, "
    "please consider reaching out to someone you trust, or call/text **988**."
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
