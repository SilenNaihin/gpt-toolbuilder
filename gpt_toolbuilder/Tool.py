# can use this class to create tools

from typing import Callable, Any, Tuple
import json
import os
from dotenv import load_dotenv
from aitemplates import create_chat_completion, Message
from .prompts.get import (
    command_results_summary_prompt,
    command_generation_prompt,
    error_summary_prompt,
)
from .prompts.prompts import TITLE_PROMPT
from gpt_toolbuilder.Environment import LinuxEnvironment
from gpt_toolbuilder.utils.Logger import Logger
from gpt_toolbuilder.utils.types import InterpreterTypes, ToolSections

load_dotenv()
BASIC_MODEL = os.environ.get("BASIC_MODEL") or "gpt-3.5-turbo"


class Tool:
    def __init__(
        self,
        title: str,
        command: str,
        environment: LinuxEnvironment,
        interpreter: InterpreterTypes = InterpreterTypes.BASH,
        description: str = "",
        tasks: list[str] = [],
    ):
        self.id = id(self)
        self.title: str = title
        self.description: str = (
            description  # TODO: vectorized in Element when Tool works
        )
        self.interpreter: InterpreterTypes = interpreter
        self.command: str = command  # completion/function, shell
        self.tasks: list[str] = tasks
        self.errors: list = []
        self.environment: LinuxEnvironment = environment
        self.logger: Logger = Logger()
        # TODO: this doesn't do anything rn
        self.section: ToolSections = ToolSections.GENERIC

        self.tests: list = []
        self.raw_results: list[str] = []
        self.results: list[str] = []

    def __call__(self, task: str) -> Tuple[bool, str]:
        result = ""
        error = False

        self.logger.debug("Using tool:", self.interpreter)
        self.logger.debug("Using bash:", InterpreterTypes.BASH)

        if self.interpreter == InterpreterTypes.BASH:
            try:
                result = self.environment.execute_shell_command(self.command)
            except Exception as e:
                error = True
                self.logger.dev("Error:", f"{e}")
        elif self.interpreter == InterpreterTypes.PYTHON:
            try:
                result = self.environment.execute_python_script(self.command)
            except Exception as e:
                error = True
                self.logger.dev("Error:", f"{e}")
        else:
            error = True
            raise NotImplementedError(
                "Interpreter type not supported. Currently only linux commands like bash are supported"
            )
        summarization: str = self.summarize_tool_use(task, result)
        self.raw_results.append(result)
        self.results.append(summarization)
        return error, summarization

    def improve_tool(self, error: Exception) -> None:
        # TODO: Read through this for v2: https://arxiv.org/pdf/2306.09896.pdf
        # TODO: feedback given context and error message
        # TODO: modify existing tool
        pass

    @staticmethod
    def create_tool(task: str, env: LinuxEnvironment) -> "Tool":
        # make it so that the fundamental building blocks are:
        # 1. shell commands
        # TODO: 2. python functions (file creation template?)
        # TODO: 3. create chat completion
        # maybe api calls from a given lib for guidance
        unix_command_msg = Message("system", command_generation_prompt(task))
        response = create_chat_completion([unix_command_msg])  # create title with 3.5
        task_command = json.loads(response)
        # tool_func = parse_response(response) # TODO: parse created function (black, linter, etc)

        Logger().dev("Tool creation command json: ", task_command)

        title = Tool.generate_title(f"{task}\n{task_command}")

        Logger().dev("Tool generated title: ", title)
        return Tool(title, task_command, env)

    def fail_reason(self) -> str:
        fail_summary_msg = Message("system", error_summary_prompt(self.errors))
        return create_chat_completion([fail_summary_msg])

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

    @staticmethod
    def generate_title(context) -> str:
        title_msg = Message("system", TITLE_PROMPT)
        context_msg = Message("system", context)
        return create_chat_completion([title_msg, context_msg], model=BASIC_MODEL)

    def test_tool(self):
        pass

    def add_desc(self, description: str) -> None:
        self.description = description

    def summarize_tool_use(self, task: str, result: str) -> str:
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
            summary = create_chat_completion(
                Message("system", command_results_summary_prompt(task, chunk)),
                model=BASIC_MODEL,
            )
            chunk_summaries.append(summary[:cutoff])

        if len(chunk_summaries) == 1:
            return chunk_summaries[0]

        summary = create_chat_completion(
            Message(
                "system",
                command_results_summary_prompt(task, "\n".join(chunk_summaries))[
                    :cutoff
                ],
            ),
            model=BASIC_MODEL,
        )

        return summary
