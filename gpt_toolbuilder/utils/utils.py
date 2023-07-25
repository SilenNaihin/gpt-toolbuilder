from .prompts import EXPAND_PROMPT
from gpt_toolbuilder.utils.types import Message
from gpt_toolbuilder.utils.chat_completion import create_chat_completion


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
        model="gpt-3.5-turbo",
        temperature=0.7,
    )

    return response.message.content
