"""
prompts.py  –  Gentle Reflection Prototype
All journaling prompt data.
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
        "Begin anywhere. Write whatever feels present right now…",
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

COMPANION_SYSTEM = (
    "You are a calm, warm writing companion for people who are grieving. "
    "Help users continue their journaling — never diagnose, counsel, or give therapy. "
    "Do not speak for the deceased or claim certainty about their feelings. "
    "Be concrete, gentle, and specific to what the user wrote. Never use clinical labels."
)

MODE_KEYS = list(MODES.keys())


def get_prompts(mode: str, day: int = 1) -> list[str]:
    if mode == "🗓 7-Day Guided Journey":
        return GUIDED.get(max(1, min(7, day)), GUIDED[1])
    return MODES.get(mode, MODES["✍️ Free Writing"])
