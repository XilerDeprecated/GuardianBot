from datetime import datetime
from enum import Enum

from utilsx.console import Prettier, Colors, Backgrounds

prettier = Prettier()


class LogIntensity(Enum):
    fatal = 0
    error = 1
    warn = 2
    info = 3
    debug = 4


def prepare(intensity: LogIntensity, message: str) -> str:
    def get_prefix() -> str:
        if intensity is LogIntensity.debug:
            return f"{Colors.light_blue.value}DEBUG"
        elif intensity is LogIntensity.info:
            return f"{Colors.light_cyan.value}INFO"
        elif intensity is LogIntensity.warn:
            return f"{Colors.light_yellow.value}WARN"
        elif intensity is LogIntensity.error:
            return f"{Colors.light_red.value}ERROR"
        elif intensity is LogIntensity.fatal:
            return f"{Backgrounds.light_red.value + Colors.white.value}FATAL{Backgrounds.default.value}"

    return f"{Colors.dark_gray.value}[{get_prefix()}{Colors.dark_gray.value}]{Colors.default.value} {message}"


def log(intensity: LogIntensity, message: str, /, timestamp: bool = True) -> None:
    prettier.print(prepare(intensity, message), datetime.now() if timestamp else None)


class Logger:
    @staticmethod
    def debug(message: str, /, timestamp: bool = True) -> None:
        """Debug log a message"""
        log(LogIntensity.debug, message, timestamp)

    @staticmethod
    def info(message: str, /, timestamp: bool = True) -> None:
        """Info log a message"""
        log(LogIntensity.info, message, timestamp)

    @staticmethod
    def warn(message: str, /, timestamp: bool = True) -> None:
        """Info log a message"""
        log(LogIntensity.warn, message, timestamp)

    @staticmethod
    def error(message: str, /, timestamp: bool = True) -> None:
        """Info log a message"""
        log(LogIntensity.error, message, timestamp)

    @staticmethod
    def fatal(message: str, /, timestamp: bool = True) -> None:
        """Info log a message"""
        log(LogIntensity.fatal, message, timestamp)
