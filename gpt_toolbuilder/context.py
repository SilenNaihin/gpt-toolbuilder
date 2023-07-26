from .prompts.prompts import TITLE_PROMPT
from utils.types import Message
from utils.chat_completion import create_chat_completion
from .prompts.get import command_results_summary_prompt


def generate_title(context) -> str:
    title_msg = Message("system", TITLE_PROMPT)
    context_msg = Message("system", context)
    r_dict = create_chat_completion(
        messages=[title_msg.raw(), context_msg.raw()],
        model=BASIC_MODEL,
        temperature=0.4,
    )

    return r_dict.message.content


def summarize_tool_use(task: str, result: str) -> str:
    cutoff = 300

    if (
        len(result) <= cutoff
    ):  # this needs to be easily used as context which is why its this low
        return result

    chunk_size = 4096

    chunk_summaries = list()
    for i in range(len(result) // chunk_size):
        chunk = result[i : i * chunk_size]
        if not chunk:
            break

        chunk_msg = Message("system", command_results_summary_prompt(task, chunk))
        summary = create_chat_completion(
            messages=[chunk_msg.raw()],
            model=BASIC_MODEL,
            temperature=0,
        )

        chunk_summaries.append(summary.message.content[:cutoff])

    if len(chunk_summaries) == 1:
        return chunk_summaries[0]

    complete_summary = Message(
        "system",
        command_results_summary_prompt(task, "\n".join(chunk_summaries))[:cutoff],
    )
    summary = create_chat_completion(
        messages=[complete_summary.raw()],
        model=BASIC_MODEL,
        temperature=0,
    )

    return summary.message.content
