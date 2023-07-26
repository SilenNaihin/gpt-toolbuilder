from gpt_toolbuilder.Tool import Tool


def tool_init(task: str, expanded_task: str):
    tool_prompt = f"{task} \n_____________\n {expanded_task}"
    # similar_tools = self.element.memory.query([tool_prompt])

    # if similar_tools:
    #     if similar_tools[0].score > 98:
    #         tool = similar_tools[0]
    #         new_tool = False
    #     else: # query retrieval set to above 80
    #         tool = Ion.merge_tools(similar_tools, tool_prompt)
    # else:
    return Tool.create_tool(tool_prompt)


def verify_tool(tool: Tool):
    # verify_syntax = syntax_verification(tool)
    # if not syntax:
    # break

    # linux_msg = Message("system", LINUX_PROMPT)
    # goal_msg = Message("user", tool.code)
    # modify_pair = FunctionPair(MODIFY_TOOL_DESC, tool.modify_tool)
    # functions = Functions([modify_pair])
    # verify_linux = create_chat_completion([linux_msg, goal_msg], functions=functions)
    pass
