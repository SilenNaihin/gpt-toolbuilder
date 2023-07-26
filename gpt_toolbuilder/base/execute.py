import subprocess
from typing import Optional

from gpt_toolbuilder.utils.Logger import Logger

logger = Logger()


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
