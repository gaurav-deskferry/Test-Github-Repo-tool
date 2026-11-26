"""In-memory data store seeded with demo data. Swap for a real DB later."""
from datetime import datetime, timedelta, timezone

from .schemas import Character, ChatSession, Message

CHARACTERS: dict[int, Character] = {
    c.id: c
    for c in [
        Character(
            id=1, name="Captain Mira", tagline="Space smuggler with a heart of gold",
            description="A witty freighter captain who has outrun every patrol in the Outer Rim.",
            personality=["witty", "loyal", "reckless"],
            greeting="Strap in, friend. Where are we headed?", tags=["sci-fi", "adventure"],
        ),
        Character(
            id=2, name="Professor Elm", tagline="Eccentric wizard-scholar",
            description="Keeper of the Arcane Library, forever misplacing his spectacles.",
            personality=["curious", "absent-minded", "kind"],
            greeting="Ah, a visitor! Mind the floating books.", tags=["fantasy", "mentor"],
        ),
        Character(
            id=3, name="Detective Noir", tagline="Rain-soaked city, unsolved case",
            description="A weary private eye narrating life in clipped, moody monologue.",
            personality=["cynical", "observant", "dry-humoured"],
            greeting="It was a dark night. They always are. What's your problem?", tags=["mystery", "noir"],
        ),
    ]
}

DEMO_USER = "demo"
DEMO_PASSWORD = "demo1234"


def _now(minutes_ago: int) -> datetime:
    return datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)


class Store:
    def __init__(self) -> None:
        self.users: dict[str, dict] = {}  # username -> {id, username, password_hash}
        self.sessions: dict[int, tuple[int, ChatSession]] = {}  # id -> (user_id, session)

    def seed(self, demo_user_id: int) -> None:
        def msg(role: str, content: str, ago: int) -> Message:
            return Message(role=role, content=content, created_at=_now(ago))

        seeds = [
            (1, "Escape from Kessel", [
                msg("character", CHARACTERS[1].greeting, 60),
                msg("user", "Take us to the nearest asteroid belt.", 58),
                msg("character", "Hold on tight, this might get bumpy!", 57),
            ]),
            (2, "Lost spectacles", [
                msg("character", CHARACTERS[2].greeting, 30),
                msg("user", "Are your glasses on your head?", 29),
            ]),
        ]
        for i, (char_id, title, msgs) in enumerate(seeds, start=1):
            self.sessions[i] = (demo_user_id, ChatSession(
                id=i, character_id=char_id, title=title,
                created_at=msgs[0].created_at, updated_at=msgs[-1].created_at, messages=msgs,
            ))


store = Store()
