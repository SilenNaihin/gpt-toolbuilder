import click

from gpt_toolbuilder.Tool import Tool
from gpt_toolbuilder.utils.Logger import Logger, ColorCode
from gpt_toolbuilder.utils.utils import expand_task
from gpt_toolbuilder.Environment import LinuxEnvironment


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
    "tool_fail_condition",
    type=int,
    default=5,
    help="Home many iterations to get the tool correct.",
)
def main(task: str, workspace: str, tool_fail_condition: int = 5):
    """Your main function for task execution."""
    logger = Logger()

    # maybe a prompt that automatically calls on of these functions?
    tool: Tool
    new_tool = True

    expanded_task = expand_task(task)

    tool_fail_count = 0
    while tool_fail_condition != tool_fail_count:
        tool_prompt = f"{task} \n_____________\n {expanded_task}"
        # similar_tools = self.element.memory.query([tool_prompt])

        # if similar_tools:
        #     if similar_tools[0].score > 98:
        #         tool = similar_tools[0]
        #         new_tool = False
        #     else: # query retrieval set to above 80
        #         tool = Ion.merge_tools(similar_tools, tool_prompt)
        # else:
        tool = Tool.create_tool(tool_prompt, LinuxEnvironment())

        # verify_syntax = syntax_verification(tool)
        # if not syntax:
        # break

        # linux_msg = Message("system", LINUX_PROMPT)
        # goal_msg = Message("user", tool.code)
        # modify_pair = FunctionPair(MODIFY_TOOL_DESC, tool.modify_tool)
        # functions = Functions([modify_pair])
        # verify_linux = create_chat_completion([linux_msg, goal_msg], functions=functions)
        output_summary = None
        try:
            # test_tool(tool) # predefined unit tests or automatically created ones
            output_summary = tool(
                expanded_task
            )  # use the tool and get summary of output

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
    main()
