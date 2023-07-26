import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

INTERACTIVE = os.getenv("INTERACTIVE")
IS_INTERACTIVE = INTERACTIVE.lower() == "true" if INTERACTIVE else False

from gpt_toolbuilder.db.db import Database as Db


def ask_user_feedback(feedback_to: str, mock_input: Optional[str] = "\n"):
    """Gets user feedback at the end of each step."""
    if not IS_INTERACTIVE:
        user_input = mock_input
    else:
        user_input = input("Provide feedback or press enter to continue: ")

    Db.add_entry("user_feedback", {"input": user_input, "to": feedback_to})
    return user_input.strip() if user_input else None
