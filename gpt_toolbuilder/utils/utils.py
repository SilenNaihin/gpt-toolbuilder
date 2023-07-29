import json

from .prompts import EXPAND_PROMPT
from gpt_toolbuilder.utils.types import Message
from gpt_toolbuilder.utils.chat_completion import create_chat_completion
from gpt_toolbuilder.utils.Logger import Logger
from gpt_toolbuilder.main import BASIC_MODEL

logger = Logger()


def list_to_num_string(lst: list) -> str:
    """
    Given a list, return a string that represents the list as a numbered list,
    with each item on a new line.
    """
    return "\n".join([f"{i+1}. {element}" for i, element in enumerate(lst)])


def expand_task(task: str) -> str:
    # TODO: another prompt here that asks if there are any assumptions etc to ask feedback from user
    # self.clarify_assumptions(self.current_task.description)

    expanded_prompt = Message("system", EXPAND_PROMPT)
    description_prompt = Message("user", task)

    response = create_chat_completion(
        messages=[expanded_prompt.raw(), description_prompt.raw()],
        model=BASIC_MODEL,
        temperature=0.7,
    )

    return response.message.content


def load_completion_json(json_str: str, format_examples: str) -> dict:
    try:
        json_obj = json.loads(json_str)
    except Exception as e:
        logger.dev("Json failed to load, retrying", e)
        json_msg = Message("system", format_json_prompt(json_str, format_examples))
        response = create_chat_completion(
            messages=[json_msg.raw()], model=BASIC_MODEL, temperature=0
        )
        json_obj = json.loads(response.message.content)

    return json_obj
