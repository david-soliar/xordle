from dataclasses import dataclass
from string import ascii_lowercase
import pathlib

from . import data_manipulator
from .logger import XordleLogger


class Data:
    __slots__ = ["words", "character_frequency", "top", "yellow", "gray", "green1", "green2", "logger", "total_top"]

    def __init__(self, enable_logging):
        self.words = data_manipulator.load_words()
        self.character_frequency = data_manipulator.load_character_frequency()

        self.top = len(self.words) - 1
        self.total_top = self.top

        self.yellow = color_list()
        self.gray = color_list()

        self.green1 = ["", "", "", "", ""]
        self.green2 = ["", "", "", "", ""]

        self.logger = XordleLogger(enable_logging=enable_logging)

    def __iter__(self):
        yield from self.words


class EmulatorData:
    __slots__ = ["words", "top", "logger", "real_xordle_games"]

    def __init__(self, enable_logging):
        self.words = data_manipulator.load_words()

        self.top = len(self.words) - 1

        self.logger = XordleLogger(enable_logging=enable_logging)

        with pathlib.Path(__file__).parent.joinpath("xordle.org.txt").open(mode="r") as file:
            self.real_xordle_games = [line.split() for line in file.readlines()]

    def __iter__(self):
        yield from self.words


@dataclass
class Color:
    __slots__ = ['indexes', 'at_least']

    indexes: list
    at_least: int


def color_list():
    data = dict()

    for ch in ascii_lowercase:
        data[ch] = Color(indexes=[0, 0, 0, 0, 0], at_least=0)
    return data
