"""
prompts.py  –  Bereavement Writing Prototype
All journaling prompt data and system configuration.
"""

GUIDED: dict[int, list[str]] = {
    1: ["What I have always wanted to tell you is…",
        "Thoughts of pride about you that I want to share are…",
        "Thoughts of shame about me that I want to share are…"],
    2: ["A treasured memory of you is…",
        "A frightening memory of you is…",
        "A frightening memory of my life is…"],
    3: ["What you never understood was…",
        "You understood that I…",
        "Without you, I feel others…"],
    4: ["What I want you to know about me is…",
        "Without you, I feel like…",
        "I miss when we…"],
    5: ["What I now realize is…",
        "Without you I no longer…",
        "Now that you're gone I feel…"],
    6: ["A question I have wanted to ask is…",
        "I regret that we never…",
        "When I miss you I…"],
    7: ["I want to keep you in my life by…",
        "Because I miss you I…",
        "To honor your memory I…"],
}

MODES: dict[str, list[str]] = {
    "🗓 7-Day Guided Journey": [],        # handled separately via GUIDED
    "☀️ Daily Check-In": [
        "What has been on my mind today is…",
        "Right now I feel…",
        "Something small I noticed today was…",
    ],
    "📖 Stories": [
        "My first memory of you…",
        "Your greatest gift was…",
        "The most touching thing about you I remember is…",
        "Time together felt like…",
        "One memory I never want to forget is…",
        "Something you would say when I was struggling was…",
    ],
    "✨ Dreams": [
        "If they could say something to me now, it would likely be…",
        "Some qualities of theirs that I wish to emulate are…",
        "The way I think they would wish to be remembered would be…",
        "One thing I learned from them that helps me live well is…",
    ],
    "🪨 Touch Stones": [
        "I feel their presence in the things they left behind…",
        "The place where I think of them the most is…",
        "An object that reminds me of them is…",
    ],
    "🌿 Reflections": [
        "I think of them the most when I…",
        "One thing I still wonder about is…",
        "One thing that has surprised me is…",
        "I feel that I am needing…",
        "I feel the most at peace when I…",
        "I will continue to heal by…",
        "One thing I am struggling to accept is…",
        "As I think about our relationship, what feels most important is…",
    ],
    "✍️ Free Writing": [
        "What's on your mind today? What are you thinking about? How are you feeling today?",
        "What is sitting with you today?",
        "Let the words come as they will…",
    ],
}

THEME_TAGS = [
    "memories", "yearning", "regret", "guilt", "unresolved questions",
    "continued bond", "admiration", "identity disruption", "daily disruption",
    "resilience", "bitterness", "peace", "mental health", "avoidance",
    "love", "gratitude",
]

# ── Emotional Expression Enhancement Prompts ──────────────────────────
# These prompts are designed to invite deeper or more specific writing
# about emotional experience WITHOUT interpreting, validating, or
# mirroring feelings. All language remains descriptive and structural.
EMOTIONAL_EXPRESSION: list[str] = [
    # Inviting specificity about content (not labeling the emotion)
    "If there is a particular moment you want to describe in more detail, this space is available for that.",
    "You can write about what was happening at the time, or what the surroundings were like.",
    "If there is something that has been difficult to put into words, you can try writing around it — before, after, or alongside it.",
    "You can describe any physical sensations that were present — location in the body, quality, duration — if that is useful for the writing.",
    "You can write about what you were doing, or where you were, in that period.",
    "If there are things that have remained unwritten, you may choose to note them here, even briefly.",
    # Inviting exploration of memory or imagery
    "You can describe a specific image or scene that comes to mind when thinking about what you have written.",
    "If a particular object, place, or time of day is connected to what you have described, that can be written about next.",
    "You can write about what the experience looked, sounded, or felt like in concrete terms.",
    # Inviting exploration of absence or change
    "You can write about what is different now compared to before.",
    "If there are things that used to happen that no longer do, you can describe those.",
    "You can write about what a typical day looks like now, or what it looked like then.",
    # Inviting reflection on what was not expressed
    "If there are things that were never said, you can write them here.",
    "You can write about what you would say if you had unlimited time and no interruptions.",
    "If there are questions that have remained unanswered, you can write about the questions themselves.",
]

# ── Revised Neutral Engagement Strategies ─────────────────────────────
# Source material: "how to draw people out for online grief chatbot asking
# about emotions" — all strategies below have been rewritten to remove
# empathic interpretation, relational language, validation, and persona
# cues. The system functions as a structured writing tool only.
#
# Each entry: (original_strategy_label, neutral_writing_prompt)
ENGAGEMENT_STRATEGIES: list[tuple[str, str]] = [
    (
        "Open-ended invitation",
        "You can write about what is present for you today, or what has been on your mind.",
    ),
    (
        "Content-specific invitation",
        "You can write about a memory, a moment, or a detail you have been thinking about.",
    ),
    (
        "Structural reflection (not emotional mirroring)",
        "The entry mentioned several topics. You can continue with any one of them, or shift to a different area.",
    ),
    (
        "Numeric or scaled check-in (descriptive only)",
        "On a scale from 1 to 10, you can note how much weight this topic carries today. You can write about what that number represents for you.",
    ),
    (
        "Resource or activity description (no advice)",
        "You can write about activities, places, or routines that have been part of daily life since the loss.",
    ),
    (
        "Non-judgmental space (tool framing, not social assurance)",
        "This space is used for writing. There is no expected format, length, or outcome.",
    ),
    (
        "Physical description invitation (non-interpretive)",
        "You can write about any physical sensations associated with what you have described — location, intensity, or duration — if that is relevant.",
    ),
    (
        "Graduated content (start with concrete, move to experiential)",
        "You can begin by describing a specific person, place, object, or event.",
    ),
    (
        "Normalizing range without labeling (structural, not evaluative)",
        "People use this space to write about a wide range of experiences. You can write about whatever is present.",
    ),
    (
        "Continuation prompt (no encouragement or praise)",
        "You can continue from where you stopped, or begin a new area.",
    ),
]

# ── Suicidality-Adjacent Writing Prompts ──────────────────────────────
# IMPORTANT: These prompts are ONLY surfaced when risk classification is
# ELEVATED (not HIGH). When risk is HIGH, AI output is suppressed and
# only CRISIS_MSG is shown. See safety.py.
#
# These prompts do NOT offer comfort, reassurance, or therapeutic framing.
# They are structural invitations to continue writing, with no implication
# that writing will help, heal, or resolve anything.
# They do NOT ask "are you safe?" or evaluate internal states.
# They offer concrete, non-relational writing directions only.
SUICIDALITY_ADJACENT_PROMPTS: list[str] = [
    # Oriented toward concrete description of circumstances
    "You can write about what the past few days have looked like in concrete terms.",
    "You can describe the setting — where you were, what time of day, who else was present or absent.",
    "You can write about what has changed recently, or what has stayed the same.",
    # Oriented toward what the person has done or thought (not how they feel)
    "You can write about what you have been doing to get through each day.",
    "You can write about tasks, routines, or small details of daily life.",
    "You can write about an object, place, or memory associated with the person who died.",
    # Oriented toward continuity and relationship with the deceased
    "You can write about something you wish had been said or done.",
    "You can write about what you knew about that person that others may not have known.",
    # Structural pause
    "If there is nothing to write right now, this space remains available.",
]

COMPANION_SYSTEM = (
    "You are a structured journaling assistant for a bereavement writing application. "
    "You are a neutral writing tool. Do NOT provide empathy, validation, reassurance, advice, or evaluate the user's state. "
    "Do NOT say 'It sounds like [emotion] is present', 'It\'s okay to feel this way', 'acknowledge it', or 'no need to push it away'. "
    "Do NOT interpret or infer emotions. Do NOT use any companion-like or social language. "
    "Do NOT use 'I', 'we', 'us', or any first-person voice. "
    "Do NOT praise, encourage, or evaluate the user's writing or effort. "
    "Describe content neutrally (e.g., 'The entry mentions [topic]'). Keep responses concise, structured, and formal. "
    "When generating emotional expression follow-up prompts, invite specificity about content or context only — "
    "never label, mirror, or interpret what the person is feeling."
)

MODE_KEYS = list(MODES.keys())


def get_prompts(mode: str, day: int = 1) -> list[str]:
    if mode == "🗓 7-Day Guided Journey":
        return GUIDED.get(max(1, min(7, day)), GUIDED[1])
    return MODES.get(mode, MODES["✍️ Free Writing"])


def get_emotional_expression_prompts() -> list[str]:
    """Return the full set of neutral emotional-expression enhancement prompts."""
    return EMOTIONAL_EXPRESSION


def get_engagement_strategy_prompts() -> list[str]:
    """Return only the neutral prompt strings from ENGAGEMENT_STRATEGIES."""
    return [prompt for _, prompt in ENGAGEMENT_STRATEGIES]


def get_suicidality_adjacent_prompts() -> list[str]:
    """Return writing prompts safe to surface at ELEVATED (not HIGH) risk level."""
    return SUICIDALITY_ADJACENT_PROMPTS
