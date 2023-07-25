from enum import Enum
import os
import traceback
from dotenv import load_dotenv

from gpt_toolbuilder.utils.Singleton import Singleton
from gpt_toolbuilder.utils.utils import list_to_num_string


class ColorCode(Enum):
    NORMAL = "\033[0m"  # Reset to default
    DEBUG = "\033[96m"  # Cyan
    INFO = "\033[93m"  # Yellow
    ERROR = "\033[91m"  # Red
    HEADER = "\033[95m"  # Magenta
    RESULT = "\033[92m"  # Green


class LogLevel(Enum):
    DEBUG = 1
    DEV = 2
    USER = 3


load_dotenv()

# Fetch environment variable and convert to LogLevel enum
log_level_str = os.getenv("LOG_LEVEL")
if log_level_str is not None:
    LOG_LEVEL = LogLevel[log_level_str]
else:
    LOG_LEVEL = LogLevel.USER


class Logger(metaclass=Singleton):
    log_level = LOG_LEVEL

    def debug(
        self,
        header: str,
        msg,
        color: ColorCode | None = ColorCode.ERROR,
        only_color_header: bool = False,
    ):
        self.log(
            header=header,
            msg=msg,
            level=LogLevel.DEBUG,
            color=color,
            only_color_header=only_color_header,
        )

    def dev(
        self,
        header: str,
        msg,
        color: ColorCode | None = ColorCode.DEBUG,
        only_color_header: bool = True,
    ):
        self.log(
            header=header,
            msg=msg,
            level=LogLevel.DEV,
            color=color,
            only_color_header=only_color_header,
        )

    def user(
        self,
        header: str,
        msg,
        color: ColorCode | None = ColorCode.INFO,
        only_color_header: bool = True,
    ):
        self.log(
            header=header,
            msg=msg,
            level=LogLevel.USER,
            color=color,
            only_color_header=only_color_header,
        )

    def log(
        self,
        header: str,
        msg,
        level: LogLevel | None = None,
        color: ColorCode | None = None,
        only_color_header: bool = True,
    ):
        if level is None:
            level = self.log_level

        if header is None:
            header = level.name
        if level.value >= self.log_level.value:
            if color is None:  # If no color is specified, use the level as color
                color = ColorCode[level.name]

            # Check if the msg is an exception
            if isinstance(msg, BaseException):
                # If it is, add the traceback information to the message
                tb_str = traceback.format_exception(type(msg), msg, msg.__traceback__)
                tb_str = "".join(
                    tb_str
                )  # This will hold the entire traceback as a string
                msg = f"{msg}\n{tb_str}"  # Append the traceback string to the original message

            if isinstance(msg, list):
                # Format the list elements as a numbered list
                msg = list_to_num_string(msg)

            if only_color_header:
                print(f"{color.value}{header}{ColorCode.NORMAL.value}{msg}")
            else:
                print(f"{color.value}{header}{msg}{ColorCode.NORMAL.value}")

    def iteration(self, iteration: str | int):
        self.log(
            "",
            f"\033[1m============= Iteration {iteration} =============\033[0m",
            level=LogLevel.USER,
            color=ColorCode.HEADER,
            only_color_header=False,
        )

    def set_level(self, level: LogLevel):
        self.log_level = level
