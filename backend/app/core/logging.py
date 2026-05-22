from enum import Enum


class Logger:
    class Level(Enum):
        INFO = "\033[94m" # Blue
        PASS = "\033[92m" # Green
        FAIL = "\033[91m" # Red
        WARN = "\033[33m" # Yellow
        ACTN = "\033[38;2;255;165;0m" # Orange
    SECTION = "\033[95m" # Purple
    RESET = "\033[0m" # Default (Reset)

    @staticmethod
    def section(title):
        print(f"\n{Logger.SECTION}=== {title} ==={Logger.RESET}")
    
    @staticmethod
    def separator(char="-", length=40):
        print(f"{char * length}")

    @staticmethod
    def newline():
        print()

    @staticmethod
    def log(message, level=None):
        if level is None:
            level = Logger.Level.INFO
        print(f"{level.value}[{level.name}]{Logger.RESET}: {message}")
    
    @staticmethod
    def info(message): Logger.log(message, Logger.Level.INFO)
    @staticmethod
    def success(message): Logger.log(message, Logger.Level.PASS)
    @staticmethod
    def fail(message): Logger.log(message, Logger.Level.FAIL)
    @staticmethod
    def warn(message): Logger.log(message, Logger.Level.WARN)
    @staticmethod
    def action(message): Logger.log(message, Logger.Level.ACTN)