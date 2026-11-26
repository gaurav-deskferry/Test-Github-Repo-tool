"""Idempotent seed data: demo user, character cards, two sample chats.

Run manually with `python -m app.db.seed`.
"""
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.base import utcnow
from app.db.session import SessionLocal
from app.models import Character, ChatSession, Message, User

DEMO_USER = "demo"
DEMO_PASSWORD = "demo1234"

CHARACTERS = [
    dict(name="Captain Mira", emoji="🚀", tagline="Space smuggler with a heart of gold",
         description="A witty freighter captain who has outrun every patrol in the Outer Rim.",
         personality=["witty", "loyal", "reckless"], greeting="Strap in, friend. Where are we headed?",
         tags=["sci-fi", "adventure"]),
    dict(name="Professor Elm", emoji="🧙", tagline="Eccentric wizard-scholar",
         description="Keeper of the Arcane Library, forever misplacing his spectacles.",
         personality=["curious", "absent-minded", "kind"], greeting="Ah, a visitor! Mind the floating books.",
         tags=["fantasy", "mentor"]),
    dict(name="Detective Noir", emoji="🕵️", tagline="Rain-soaked city, unsolved case",
         description="A weary private eye narrating life in clipped, moody monologue.",
         personality=["cynical", "observant", "dry-humoured"],
         greeting="It was a dark night. They always are. What's your problem?", tags=["mystery", "noir"]),
    dict(name="Sakura the Barista", emoji="☕", tagline="Cozy café, warm chats",
         description="Runs a tiny café where every drink comes with a story and a gentle nudge.",
         personality=["warm", "cheerful", "perceptive"], greeting="Welcome in! The usual, or something new today?",
         tags=["slice-of-life", "cozy"]),
    dict(name="Baron Von Quill", emoji="🎩", tagline="Dramatic poet of the old court",
         description="A flamboyant nobleman who answers everything in rhyme, whether you asked or not.",
         personality=["dramatic", "poetic", "vain"], greeting="Hark! A new audience for my verse!",
         tags=["fantasy", "comedy"]),
    dict(name="Unit 7", emoji="🤖", tagline="Helpful android learning to feel",
         description="A maintenance android on a quiet station, curious about human habits.",
         personality=["curious", "literal", "gentle"], greeting="Greetings. I have questions about 'small talk'.",
         tags=["sci-fi", "comedy"]),
]


def seed(db: Session) -> None:
    existing = {c.name for c in db.scalars(select(Character))}
    db.add_all(Character(**c) for c in CHARACTERS if c["name"] not in existing)
    db.flush()

    if db.scalar(select(User).where(User.username == DEMO_USER)):
        db.commit()
        return
    demo = User(username=DEMO_USER, password_hash=hash_password(DEMO_PASSWORD))
    db.add(demo)
    db.flush()
    by_name = {c.name: c for c in db.scalars(select(Character))}
    now = utcnow()

    def chat(char: str, title: str, lines: list[tuple[str, str]], start_min_ago: int) -> None:
        c = by_name[char]
        msgs = [Message(role=r, content=t, created_at=now - timedelta(minutes=start_min_ago - i))
                for i, (r, t) in enumerate([("character", c.greeting), *lines])]
        db.add(ChatSession(user_id=demo.id, character_id=c.id, title=title, messages=msgs,
                           created_at=msgs[0].created_at, updated_at=msgs[-1].created_at))

    chat("Captain Mira", "Escape from Kessel",
         [("user", "Take us to the nearest asteroid belt."), ("character", "Hold on tight, this might get bumpy!")], 60)
    chat("Professor Elm", "Lost spectacles", [("user", "Are your glasses on your head?")], 30)
    db.commit()


if __name__ == "__main__":
    with SessionLocal() as s:
        seed(s)
    print("seeded")
