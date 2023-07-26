import click
from typing import Optional
from pathlib import Path
import os
from dotenv import load_dotenv

from gpt_toolbuilder.utils.types import InterpreterTypes

load_dotenv()

REPORT_LOCATION = os.getenv("REPORT_LOCATION")
REPORT_LOCATION = (
    Path(REPORT_LOCATION).resolve() if REPORT_LOCATION else Path.cwd() / "reports"
)


from gpt_toolbuilder.Tool import Tool
from gpt_toolbuilder.utils.Logger import Logger, ColorCode
from gpt_toolbuilder.utils.utils import expand_task
from gpt_toolbuilder.decisions import tool_init, verify_tool
from gpt_toolbuilder.actions import Templates
from gpt_toolbuilder.db.db import Database as Db
from gpt_toolbuilder.base.Input import ask_user_feedback


@click.command()
@click.argument(
    "task",
    type=str,
    required=True,
    help="The task that the tool needs to be completed for.",
)
@click.argument(
    "workspace",
    type=str,
    default="gpt_toolbuilder/tool_library/generated",
    help="The workspace to store the generated tools in.",
)
@click.argument(
    "fail_condition",
    type=int,
    default=5,
    help="Home many iterations to get the tool correct.",
)
def tbuild(
    task: str,
    workspace: str,
    fail_condition: Optional[int] = 5,
    mock_input: str = "\n",
    template: Templates = Templates.DEFAULT,
    interpreter: list[str] = ["python", "shell"],
):
    """Your main function for task execution."""
    logger = Logger()

    Db().initialize(REPORT_LOCATION)

    for action in template.value:
        print(action)

    expanded_task = expand_task(task)

    # tool_prompt = # TODO: task -> tool `write hello to a file` -> `write file tool`

    tool_fail_count = 0
    new_tool = True
    tool: Tool
    while fail_condition != tool_fail_count:
        tool = tool_init(task, expanded_task)
        verify = verify_tool(tool)

    # maybe a prompt that automatically calls on of these functions?

    output_summary = None
    try:
        # test_tool(tool) # predefined unit tests or automatically created ones
        output_summary = tool(expanded_task)  # use the tool and get summary of output

        logger.dev(
            "Summary of tool usage output: ",
            f"error: {output_summary[0]}, summary: {output_summary[1]}",
        )

        # task_pair = self.element.memory.add("task", [tool_prompt], metadata={"tool": tool.id})

        # if made it here it's a success
        # if new_tool:
        #     tool.add_desc()
        # tool_pair = self.element.memory.add("tool", [tool.name + tool.description + tool.errors], metadata={"tasks": [task.id for task in tool.tasks], "tool": tool.id})
        # else:
        # tool_pair = self.element.memory.update("tool", where={"tool": tool.id}, metadata={"tasks": [task.id for task in tool.tasks]})

        # if no error, maybe was the task done correctly prompt?
        # maybe we predict what the env will look like next and if it doesn't match it's a failure/not a success?

        return output_summary  # (error: bool, summary: str)

    except Exception as e:
        logger.dev(
            "Error executing task: ",
            e,
            color=ColorCode.ERROR,
        )

        tool_fail_count += 1
        # remainder = count % 3

        # TODO: Tool master prompt to choose this automatically
        #   improve tool
        #   gain context
        #   search for info

        ask_user_feedback("tool", mock_input)

        tool.errors.append(e)

        # if remainder == 1:  # This corresponds to counts 1, 4, 7, etc.
        tool.improve_tool(e)
        # elif remainder == 2:  # This corresponds to counts 2, 5, 8, etc
        #     info = search_for_info()
        #     tool.improve_tool(e, info)
        # elif remainder == 0:  # This corresponds to counts 3, 6, 9, etc.
        #     # some sort of algo here to choose best way to generate seed tool
        #     tool = tool.create_tool(e)

        # think,

    fail_reason = tool.fail_reason()
    return fail_reason


if __name__ == "__main__":
    tbuild()
