# can use this class to create tools

from typing import Tuple
import json
import os
from dotenv import load_dotenv
from utils.types import Message
from utils.chat_completion import create_chat_completion
from .prompts.get import (
    command_generation_prompt,
    error_summary_prompt,
)
from .context import generate_title, summarize_tool_use
from gpt_toolbuilder.base.Environment import LinuxEnvironment
from gpt_toolbuilder.utils.Logger import Logger
from gpt_toolbuilder.utils.types import ToolSections
from gpt_toolbuilder.base.execute import execute_shell_command, execute_python_script

load_dotenv()
BASIC_MODEL = os.environ.get("BASIC_MODEL") or "gpt-3.5-turbo"


class Tool:
    def __init__(
        self,
        title: str,
        command: str,
        interpreter: list[str],
        description: str = "",
        tasks: list[str] = [],
    ):
        self.id = id(self)
        self.title = title
        self.description: str = (
            description  # TODO: vectorized in Element when Tool works
        )
        self.interpreter = interpreter
        self.command = command  # completion/function, shell
        self.tasks: list[str] = tasks
        self.errors: list = []
        self.environment = LinuxEnvironment()
        self.logger: Logger = Logger()
        # TODO: this doesn't do anything rn
        self.section: ToolSections = ToolSections.GENERIC

        self.tests: list = []
        self.raw_results: list[str] = []
        self.results: list[str] = []

    def __call__(self, task: str) -> Tuple[bool, str]:
        result: str | None = ""
        error = False

        self.logger.debug("Using tool:", self.interpreter)

        if "bash" in self.interpreter:
            try:
                result = execute_shell_command(self.command)
            except Exception as e:
                error = True
                self.logger.dev("Error:", f"{e}")
        elif "python" in self.interpreter:
            try:
                result = execute_python_script(self.command)
            except Exception as e:
                error = True
                self.logger.dev("Error:", f"{e}")
        else:
            error = True
            raise NotImplementedError(
                "Interpreter type not supported. Currently only linux commands like bash are supported"
            )
        summarization: str = summarize_tool_use(task, result)
        self.raw_results.append(result)
        self.results.append(summarization)
        return error, summarization

    def improve_tool(self, error: Exception) -> None:
        # TODO: Read through this for v2: https://arxiv.org/pdf/2306.09896.pdf
        # TODO: feedback given context and error message
        # TODO: modify existing tool
        pass

    @staticmethod
    def create_tool(task: str, interpreter: list[str]) -> "Tool":
        # make it so that the fundamental building blocks are:
        # 1. shell commands
        # TODO: 2. python functions (file creation template?)
        # TODO: 3. create chat completion
        # maybe api calls from a given lib for guidance
        unix_command_msg = Message("system", command_generation_prompt(task))
        response = create_chat_completion(
            messages=[unix_command_msg.raw()], model=COMPLEX_MODEL, temperature=0.2
        )

        task_command = json.loads(response)
        # tool_func = parse_response(response) # TODO: parse created function (black, linter, etc)

        Logger().dev("Tool creation command json: ", task_command)

        title = generate_title(f"{task}\n{task_command}")

        Logger().dev("Tool generated title: ", title)
        return Tool(title, task_command, interpreter)

    def fail_reason(self) -> str:
        fail_summary_msg = Message("system", error_summary_prompt(self.errors))
        response = create_chat_completion(
            messages=[fail_summary_msg.raw()], model=COMPLEX_MODEL, temperature=0.2
        )
        return response.message.content

    @staticmethod
    def merge_tools(*args) -> "Tool":
        # create_chat_completion()
        # TODO: environments don't match error, chat completion only merged with python error
        for tool in args:
            pass

        # Tool.generate_title(task)

        # return Tool(
        #     "",
        #     "",
        #     tool_func,
        # )
