import random
import pathlib

from .data.data import EmulatorData
from .status import Status


class XordleEmulator(EmulatorData):
    def __init__(self, xordle_index=None, words=None, clue_word=None, enable_logging=False):
        super().__init__(enable_logging=enable_logging)

        if isinstance(xordle_index, int):
            xordle_index = xordle_index % 40000
            self.clue_word, self.emulator_word1, self.emulator_word2 = self.real_xordle_games[xordle_index]

        elif words and len(words) == 2 and not bool(set(words[0]) & set(words[1])):
            self.emulator_word1 = words[0]
            self.emulator_word2 = words[1]
            self.clue_word = clue_word

        else:
            if words:
                raise Exception(f"words are not disjunct or something else idk")

            self.emulator_word1 = self.words[random.randint(0, self.top)].word
            self.emulator_word2 = self.words[random.randint(0, self.top)].word
            while bool(set(self.emulator_word1) & set(self.emulator_word2)):
                self.emulator_word2 = self.words[random.randint(0, self.top)].word
            self.clue_word = self.words[random.randint(0, self.top)].word

        self.MAX_GUESSES = 8
        self._current_guess = 0
        self._guessed = 0
        self.status = Status.NONE
        self.huh = False
        self.already_guessed = list()
        self.already_guessed_colors = list()

    def _exceeded_max_guesses(self):
        return self._current_guess > self.MAX_GUESSES

    def start(self):
        if self.status != Status.NONE:
            return None, None

        self.status = Status.IN_PROGRESS

        color = self._calculate_color(self.clue_word)
        self.huh = (color == "22222" and (self.clue_word != self.emulator_word1 and self.clue_word != self.emulator_word2))
        self.already_guessed.append(self.clue_word)
        self.already_guessed_colors.append(color)
        if self.clue_word == self.emulator_word1 or self.clue_word == self.emulator_word2:
            self._guessed += 1
        return (self.clue_word, color)

    def guess(self, word):
        self.huh = False

        if self.status == Status.LOSS or self.status == Status.WIN:
            return None

        if self._exceeded_max_guesses():
            self.status = Status.LOSS
            return None

        if word in self.already_guessed:
            self.status = Status.ALREADY_GUESSED
            return None

        if not word:
            self.status = Status.NOT_VALID_WORD
            return None

        if word not in [w.word for w in self.words]:
            self.status = Status.NOT_VALID_WORD
            return None

        if self._current_guess == (self.MAX_GUESSES - 1) and self.emulator_word1 != word and self.emulator_word2 != word:
            self.status = Status.LOSS
            color = self._calculate_color(word)
            if color == "22222":
                self.huh = True
            self.already_guessed_colors.append(color)
            self.already_guessed.append(word)
            return color

        self.status = Status.IN_PROGRESS
        if self.emulator_word1 == word or self.emulator_word2 == word:
            self.already_guessed_colors.append("22222")
            self.already_guessed.append(word)
            if self._guessed == 0:
                if self.emulator_word1 == word:
                    self.emulator_word1 = None
                else:
                    self.emulator_word2 = None

                if self._current_guess == 7:
                    self._current_guess -= 1
                    self.status = Status.BONUS

                self._guessed += 1
                self._current_guess += 1
                return "22222"
            else:
                self.status = Status.WIN
                return "22222"

        color = self._calculate_color(word)
        if color == "22222":
            self.huh = True

        self.status = Status.IN_PROGRESS

        self.already_guessed.append(word)
        self._current_guess += 1
        self.already_guessed_colors.append(color)

        return color

    def _calculate_color(self, word):
        color = list("00000")

        character_frequency = dict()
        for char in word:
            character_frequency[char] = 0

        if self.emulator_word1:
            for i in range(5):
                if word[i] == self.emulator_word1[i]:
                    color[i] = "2"
                    character_frequency[word[i]] += 1

        if self.emulator_word2:
            for i in range(5):
                if word[i] == self.emulator_word2[i]:
                    color[i] = "2"
                    character_frequency[word[i]] += 1

        if self.emulator_word1:
            for i in range(5):
                if word[i] in self.emulator_word1 and character_frequency[word[i]] < self.emulator_word1.count(word[i]) and color[i] != "2":
                    color[i] = "1"
                    character_frequency[word[i]] += 1

        if self.emulator_word2:
            for i in range(5):
                if word[i] in self.emulator_word2 and character_frequency[word[i]] < self.emulator_word2.count(word[i]) and color[i] != "2":
                    color[i] = "1"
                    character_frequency[word[i]] += 1

        return "".join(color)
