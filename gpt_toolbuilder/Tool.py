# can use this class to create tools

from typing import Tuple
from gpt_toolbuilder.utils.types import Message
from gpt_toolbuilder.utils.chat_completion import create_chat_completion
from .prompts.get import error_summary_prompt
from .context import summarize_tool_use
from gpt_toolbuilder.base.Environment import LinuxEnvironment
from gpt_toolbuilder.utils.Logger import Logger
from gpt_toolbuilder.utils.types import ToolSections
from gpt_toolbuilder.base.execute import execute_shell_command, execute_python_script
from gpt_toolbuilder.main import COMPLEX_MODEL


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

    def fail_reason(self) -> str:
        fail_summary_msg = Message("system", error_summary_prompt(self.errors))
        response = create_chat_completion(
            messages=[fail_summary_msg.raw()], model=COMPLEX_MODEL, temperature=0.2
        )
        return response.message.content
