import subprocess


def execute_shell_command(self, command: str, timeout: int = 10):
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
        return self.logger.debug("Error: ", f"{e.output.strip()}")


def execute_python_script(self, function_string: str, timeout: int = 10):
    local_scope = {}
    try:
        # Use exec to execute the function_string.
        exec(function_string, {}, local_scope)
    except Exception as e:
        self.logger.debug("Error executing function: ", f"{e}")

    # The function's return value will be in the local scope with the key '_return'.
    return local_scope.get("_return")
