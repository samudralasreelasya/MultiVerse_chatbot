import sqlite3
from datetime import datetime
import pandas as pd

DB_NAME = "chat_history.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            personality TEXT,
            tone TEXT,
            role TEXT,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_message(personality, tone, role, content):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO messages (timestamp, personality, tone, role, content) VALUES (?, ?, ?, ?, ?)",
        (datetime.now().isoformat(), personality, tone, role, content)
    )
    conn.commit()
    conn.close()


def fetch_all_messages():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM messages ORDER BY timestamp DESC", conn)
    conn.close()
    return df


def fetch_stats():
    df = fetch_all_messages()
    if df.empty:
        return None

    total_messages = len(df)
    total_conversations = len(df[df["role"] == "user"])
    top_personality = df["personality"].mode()[0] if not df["personality"].empty else "N/A"
    top_tone = df["tone"].mode()[0] if not df["tone"].empty else "N/A"

    personality_counts = df["personality"].value_counts()

    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    daily_counts = df.groupby("date").size()

    return {
        "total_messages": total_messages,
        "total_conversations": total_conversations,
        "top_personality": top_personality,
        "top_tone": top_tone,
        "personality_counts": personality_counts,
        "daily_counts": daily_counts,
    }
