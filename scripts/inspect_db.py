"""
MindCare AI - SQLite Database Inspector Utility
Inspect tables, registered users, sessions, and messages in mindcare.db
"""
import sys
import os
from pathlib import Path

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from backend.app.core.database import SessionLocal
from backend.app.models.user import User
from backend.app.models.session import Session
from backend.app.models.message import Message

def inspect_database():
    print("=" * 60)
    print("MindCare AI - SQLite Database Inspector (mindcare.db)")
    print("=" * 60)

    db_path = ROOT_DIR / "mindcare.db"
    if not db_path.exists():
        print(f"[!] SQLite database file not found at: {db_path}")
        return

    print(f"Database Location: {db_path}")
    print(f"File Size: {db_path.stat().st_size / 1024:.2f} KB\n")

    with SessionLocal() as db:
        users = db.query(User).all()
        print(f"Registered Users ({len(users)}):")
        for u in users:
            print(f"  - [{u.id[:8]}...] {u.name} <{u.email}> (Created: {u.created_at})")

        sessions = db.query(Session).all()
        print(f"\nChat Sessions ({len(sessions)}):")
        for s in sessions:
            msg_count = len(s.messages) if s.messages else 0
            print(f"  - [{s.id[:8]}...] '{s.title}' (User: {s.user_id[:8]}..., Messages: {msg_count})")

        messages = db.query(Message).all()
        print(f"\nTotal Stored Messages: {len(messages)}")

    print("=" * 60)

if __name__ == "__main__":
    inspect_database()
