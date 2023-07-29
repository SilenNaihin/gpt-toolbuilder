import subprocess
import json

from gpt_toolbuilder.context import generate_title
from gpt_toolbuilder.prompts.get import command_generation_prompt
from gpt_toolbuilder.utils.Logger import Logger
from gpt_toolbuilder.Tool import Tool
from gpt_toolbuilder.utils.types import Message
from gpt_toolbuilder.utils.utils import load_completion_json
from gpt_toolbuilder.utils.chat_completion import create_chat_completion
from gpt_toolbuilder.main import COMPLEX_MODEL

logger = Logger()


def execute_command_or_script(
    command_or_script: str, is_script: bool = False, timeout: int = 10
) -> str:
    if is_script:
        return execute_python_script(command_or_script, timeout)
    else:
        return execute_shell_command(command_or_script, timeout)


def execute_shell_command(command: str, timeout: int = 10) -> str:
    try:
        output = subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            shell=True,
            text=True,
            timeout=timeout,
        )
        return output.strip()
    except subprocess.CalledProcessError as e:
        logger.debug("Error: ", f"{e.output.strip()}")
        return e.output.strip()


def execute_python_script(function_string: str, timeout: int = 10) -> str:
    local_scope = {}
    try:
        # Use exec to execute the function_string.
        exec(function_string, {}, local_scope)
    except Exception as e:
        logger.debug("Error executing function: ", f"{e}")

    # The function's return value will be in the local scope with the key '_return'.
    return_val = local_scope.get("_return")
    return return_val if return_val is not None else "Error: Return value is None"


def create_tool(task: str, interpreter: list[str], model: str) -> "Tool":
    # make it so that the fundamental building blocks are:
    # 1. shell commands
    # TODO: 2. python functions (file creation template?)
    # TODO: 3. create chat completion
    # maybe api calls from a given lib for guidance
    unix_command_msg = Message("system", command_generation_prompt(task))
    response = create_chat_completion(
        messages=[unix_command_msg.raw()], model=COMPLEX_MODEL, temperature=0.2
    )

    task_command = load_completion_json(
        response.message.content,
    )
    # tool_func = parse_response(response) # TODO: parse created function (black, linter, etc)

    logger.dev("Tool creation command json: ", task_command)

    title = generate_title(f"{task}\n{task_command}")

    logger.dev("Tool generated title: ", title)
    return Tool(title, task_command["command"], task_command["interpreter"])


def merge_tools(task: str, tool1: Tool, tool2: Tool) -> Tool:
    # TODO: arbitrary amount of tools. for tool in args:
    if tool1.interpreter != tool2.interpreter:
        raise TypeError("Interpreter types don't match.")

    combine_msg = Message("system", command_combine_prompt(task))
    response = create_chat_completion(
        messages=[combine_msg.raw()], model=COMPLEX_MODEL, temperature=0.2
    )

    new_command = load_completion_json(
        response.message.content,
    )

    title = generate_title(f"{task}\n{new_command}")

    return Tool(title, new_command["command"], new_command["interpreter"])
