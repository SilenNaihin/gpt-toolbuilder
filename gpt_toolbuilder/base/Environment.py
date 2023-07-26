# environment information, get and storage
import os
import psutil


from gpt_toolbuilder.utils.Logger import Logger


class LinuxEnvironment:
    def __init__(self):
        self.logger = Logger()

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
