from enum import Enum
from typing import Callable, Any

from gpt_toolbuilder.base.execute import (
    execute_shell_command,
    execute_python_script,
)
from gpt_toolbuilder.base.Input import ask_user_feedback


FUNCTION_MAP = {
    "shell": execute_shell_command,
    "python": execute_python_script,
    "feedback": ask_user_feedback,
}


class Actions(Enum, str):
    """This is a single action in our tool building process."""

    CLARIFY = "clarify"  # ask for clarification from assumptions
    REFINE = "refine"  # refine a tool as it doesn't perform given task
    REFLECT = "reflect"
    DEVELOP = "develop"
    VERIFY = "verify"
    EXPAND = "expand"
    FEEDBACK = "feedback"

    def get_step_function(self, step: str) -> Callable[[Any], Any]:
        function = FUNCTION_MAP.get(step)

        if function is None:
            raise ValueError(f"No function found for step: {step}")
        return function


class Loop(Enum):
    DEFAULT = [Actions.EXPAND]


class Sequences(Enum):
    ERROR = [
        Actions.REFINE,
    ]
    VERIFICATION = [
        Actions.VERIFY,
        Actions.REFLECT,
    ]


class Templates(Enum):
    DEFAULT = [
        Actions.CLARIFY,
        Loop.DEFAULT,
    ]
