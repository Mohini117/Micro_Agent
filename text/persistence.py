import json
import os
import tempfile
from datetime import datetime

from message import Message


def convert_to_dict(message):
    return {
        "role": message.role,
        "content": message.content,
        "timestamp": str(message.timestamp)
    }


def save_history(history, filepath):
    history_dicts = [convert_to_dict(msg) for msg in history]

    with open(filepath, "w") as f:
        json.dump(history_dicts, f, indent=4)


def load_history(filepath):
    with open(filepath, "r") as f:
        history_dicts = json.load(f)

    for msg_dict in history_dicts:
        msg_dict["timestamp"] = datetime.fromisoformat(msg_dict["timestamp"])

    return [Message(**msg_dict) for msg_dict in history_dicts]


if __name__ == "__main__":
    history = [
        Message("user", "What does this medicine do?"),
        Message("assistant", "It's for blood pressure.")
    ]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        filepath = tmp.name

    try:
        save_history(history, filepath)
        loaded = load_history(filepath)
    finally:
        os.remove(filepath)

    # Uncomment these while manually checking the round trip.
    # print(type(loaded[0].timestamp))
    # print(loaded[0].role)
    # print(loaded[0].content)
    # print(loaded[0].timestamp == history[0].timestamp)
