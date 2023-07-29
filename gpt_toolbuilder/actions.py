from enum import Enum
from typing import Callable, Any

from gpt_toolbuilder.base.execute import execute_command_or_script
from gpt_toolbuilder.base.Input import ask_user_feedback
from gpt_toolbuilder.utils.utils import expand_task
from gpt_toolbuilder.decisions import tool_init, verify_tool

FUNCTION_MAP = {
    "execute": execute_command_or_script,
    "feedback": ask_user_feedback,
    "expand": expand_task,
    "develop_tool": tool_init,
    "verify_tool": verify_tool,
    "user_feedback": ask_user_feedback,
}


class Actions(Enum, str):
    """This is a single action in our tool building process."""

    CLARIFY = "clarify"  # TODO: ask for clarification from assumptions
    REFINE = "refine"  # TODO: refine a tool as it doesn't perform given task
    REFLECT = "reflect"  # TODO
    DEVELOP = "develop_tool"  # TODO: tool_init vs create_tool
    VERIFY = "verify"  # TODO
    EXPAND = "expand"
    FEEDBACK = "user_feedback"
    EXECUTE = "execute"

    def get_step_function(self, step: str) -> Callable[[Any], Any]:
        function = FUNCTION_MAP.get(step)

        if function is None:
            raise ValueError(f"No function found for step: {step}")
        return function


class Loop(Enum):
    DEFAULT = {}


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
        Actions.EXPAND,
        Loop.DEFAULT,
    ]
