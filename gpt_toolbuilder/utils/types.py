from enum import Enum
from dataclasses import dataclass
from typing import Literal, Optional, TypedDict, Any

# Different roles the chat API takes
MessageRole = Literal["system", "user", "assistant", "function"]


class ToolSections(Enum):
    BROWSING = "browsing"
    API = "api"
    GENERIC = "generic"


@dataclass
class FunctionCall:
    name: str
    arguments: str


class MessageDict(TypedDict):
    role: MessageRole
    content: str


@dataclass
class Message:
    """OpenAI Message object containing a role and the message content"""

    role: MessageRole
    content: str
    function_call: Optional[FunctionCall] = None

    def raw(self) -> MessageDict:
        return {"role": self.role, "content": self.content}


@dataclass
class ResponseDict:
    index: int
    message: Message
    finish_reason: str
    model: str
    created: str

    def __init__(self, response: dict, function_response: Any = None):
        choice = response["choices"][0]  # Getting the first choice
        self.index = choice["index"]
        if function_response:
            self.message = Message("function", function_response)
        else:
            self.message = Message(**choice["message"])
        self.finish_reason = choice["finish_reason"]
        self.model = response["model"]
        self.created = response["created"]
