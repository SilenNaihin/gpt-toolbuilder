# environment information, get and storage
import os
import psutil
import subprocess

from gpt_toolbuilder.utils.Logger import Logger


class LinuxEnvironment:
    def __init__(self):
        self.logger = Logger()

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

    def current_path(self):
        return os.getcwd()

    def get_cpu_usage(self):
        """CPU usage (percentage)"""
        return str(psutil.cpu_percent()) + "%"

    def get_memory_usage(self):
        return ""

    def get_available_memory(self):
        """Available memory (MB)"""
        mem_info = psutil.virtual_memory()
        return str(mem_info.available // (1024 * 1024)) + " MB"

    def get_disk_usage(self):
        return ""

    def get_process_count(self):
        return ""

    def get_time_passed(self):
        return ""
