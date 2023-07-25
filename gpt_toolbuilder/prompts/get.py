from .prompts import (
    COMMAND_GENERATION_PROMPT,
    COMMAND_RESULTS_SUMMARY_PROMPT,
    ERROR_SUMMARY_PROMPT,
)
from gpt_toolbuilder.utils.utils import list_to_num_string


def command_generation_prompt(task: str) -> str:
    return COMMAND_GENERATION_PROMPT.format(task=task)


def command_results_summary_prompt(task: str, result: str) -> str:
    return COMMAND_RESULTS_SUMMARY_PROMPT.format(task=task, result=result)


def error_summary_prompt(errors: list) -> str:
    error_nums = list_to_num_string(errors)
    return ERROR_SUMMARY_PROMPT.format(errors=error_nums)
