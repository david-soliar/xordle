from enum import Flag, auto


class Status(Flag):
    IN_PROGRESS = auto()
    BONUS = auto()
    WIN = auto()
    LOSS = auto()
    NOT_VALID_WORD = auto()
    NONE = auto()
    ALREADY_GUESSED = auto()
    FINISHED = WIN | LOSS
