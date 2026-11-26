"""Placeholder chat engine. Replace `stub_reply` with a real model call."""
from app.models import Character

_LINES = {
    "witty": "Ha! You've got a sharp tongue. Go on, I'm listening.",
    "curious": "Hmm, fascinating! Tell me more about that.",
    "cynical": "Heard it all before. But go ahead — surprise me.",
}
_DEFAULT = "Interesting. Tell me more."


def stub_reply(character: Character, text: str) -> str:
    for trait in character.personality:
        if trait in _LINES:
            return f"{_LINES[trait]} (“{text.strip()[:60]}”)"
    return _DEFAULT
