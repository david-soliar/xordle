import logging
from pathlib import Path
from string import ascii_lowercase


class XordleLogger:
    def __init__(self, enable_logging=True):
        self.enable_logging = enable_logging
        if enable_logging:
            self.LOG_DIR = Path(__file__).parent.parent.parent.joinpath("log")
            self.LOG_FILE_PATH = self.LOG_DIR.joinpath("xordle.log")

            self.logger = logging.getLogger("xordle_logger")
            self.logger.setLevel(logging.DEBUG)

            formatter = logging.Formatter("%(message)s")

            file_handler = logging.FileHandler(self.LOG_FILE_PATH, mode='w')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

            self.log_print("LOG START")

    def _log(self, log_fun, message):
        if self.enable_logging:
            log_fun(message)

    def log_info(self, message):
        self._log(self.logger.info, message)

    def log_warning(self, message):
        self._log(self.logger.warning, message)

    def log_error(self, message):
        self._log(self.logger.error, message)

    def log_debug(self, message):
        self._log(self.logger.debug, message)

    def log_color(self, color, name):
        if self.enable_logging:
            total_sum = 0
            to_log = str()
            to_log += name + "= "
            for character in ascii_lowercase:
                str_indexes = [str(x) for x in color[character].indexes]
                to_log += f"({character}: {''.join(str_indexes)} -> {color[character].at_least})  "
                total_sum += color[character].at_least
            to_log += "\n"
            to_log += f"total sum: {total_sum}\n"
            self.logger.info(to_log)

    def log_green(self, green1, green2):
        if self.enable_logging:
            self.logger.info(f"green1: {green1}, green2: {green2}\n")

    def log_words(self, words, top, all=False):
        if self.enable_logging:
            to_log = str()
            if all:
                for i in range(top + 1):
                    to_log += f"{i}. " + words[i].word + "\n"
            to_log += f"top: {top} --> (word top: {words[top].word})\n\n"
            self.logger.info(to_log)

    def log_print(self, string):
        if self.enable_logging:
            self.logger.info(string + "\n")
