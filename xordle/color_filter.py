from string import ascii_lowercase

from .data.data import Data
from .data.timer import timer


class ColorFilter(Data):
    def __init__(self, enable_logging):
        super().__init__(enable_logging=enable_logging)

    @timer
    def update_green_color(self, actual_green):
        for i in range(5):
            if actual_green[i]:
                if self.green1[i]:
                    if self.green1[i] != actual_green[i]:
                        self.green2[i] = actual_green[i]
                else:
                    self.green1[i] = actual_green[i]

    @timer
    def infer_green_by_gray_and_yellow(self):
        for character in ascii_lowercase:
            sum = 0
            index = -1

            if self.yellow[character].at_least != 0 and (self.green1.count(character) + self.green2.count(character)) == 0:
                for i in range(5):
                    if (self.yellow[character].indexes[i] == 1 or self.gray[character].indexes == 1) or (self.green1[i] != "" and self.green2[i] != ""):
                        sum += 1
                    else:
                        index = i

                if sum == 4:
                    if self.green1[index]:
                        if not self.green2[index]:
                            self.green2[index] = character
                    else:
                        self.green1[index] = character
                    self.remove_found_yellow_by_green_position()
                    self.infer_green_by_gray_and_yellow()
                    self.infer_green_by_yellow_position()

    @timer
    def infer_green_by_yellow_position(self):
        for character in ascii_lowercase:
            sum = 0
            index1, index2 = -1, -1

            if self.yellow[character].at_least != 0 and (self.green1.count(character) + self.green2.count(character)) == 0:
                for i in range(5):
                    if (self.yellow[character].indexes[i] == 1 or self.gray[character].indexes == 1) or (self.green1[i] != "" and self.green2[i] != ""):
                        sum += 1
                    else:
                        if index1 == -1:
                            index1 = i
                        else:
                            index2 = i

                if sum == 3:
                    on_index1 = self.check_if_character_on_index_exists_in_words(character, index1)
                    on_index2 = self.check_if_character_on_index_exists_in_words(character, index2)

                    if on_index1 == on_index2:
                        continue

                    index = index1 if on_index1 else index2
                    if self.green1[index]:
                        if not self.green2[index]:
                            self.green2[index] = character
                    else:
                        self.green1[index] = character

                    self.remove_found_yellow_by_green_position()
                    self.infer_green_by_yellow_position()
                    self.infer_green_by_gray_and_yellow()

    @timer
    def remove_found_yellow_by_green_position(self):
        for i in range(5):
            char_green1 = self.green1[i]
            char_green2 = self.green2[i]

            if char_green1 != "" and self.yellow[char_green1].at_least > 0:
                if self.yellow[char_green1].at_least == 1:
                    self.yellow[char_green1].at_least = 0
                    self.yellow[char_green1].indexes = [0, 0, 0, 0, 0]
                else:
                    self.yellow[char_green1].indexes[i] = 0
                    self.yellow[char_green1].at_least -= 1

            elif char_green2 != "" and self.yellow[char_green2].at_least > 0:
                if self.yellow[char_green2].at_least == 1:
                    self.yellow[char_green2].at_least = 0
                    self.yellow[char_green2].indexes = [0, 0, 0, 0, 0]
                else:
                    self.yellow[char_green2].indexes[i] = 0
                    self.yellow[char_green2].at_least -= 1

    @timer
    def check_if_character_on_index_exists_in_words(self, character, i):
        index = 0
        while index <= self.top:
            if self.words[index].word[i] == character:
                return True
            index += 1
        return False

    @timer
    def remake_actual_colors_and_sum_it(self, actual_colors):
        actual_colors["green"] = ["" if val == "0" else val for val in actual_colors["green"]]
        actual_colors["yellow"] = ["" if val == "0" else val for val in actual_colors["yellow"]]
        actual_colors["gray"] = ["" if val == "0" else val for val in actual_colors["gray"]]

        green_sum = len([item for item in actual_colors["green"] if item != ""])
        yellow_sum = len([item for item in actual_colors["yellow"] if item != ""])
        gray_sum = len([item for item in actual_colors["gray"] if item != ""])
        return green_sum, yellow_sum, gray_sum

    @timer
    def update_colors(self, actual_colors, word, color):
        for i in range(5):
            if actual_colors["yellow"][i] in ascii_lowercase:
                occurences = 0
                for j in range(5):
                    if word[j] == actual_colors["yellow"][i] and actual_colors["yellow"][j] == actual_colors["yellow"][i]:
                        occurences += 1
                if self.yellow[actual_colors["yellow"][i]].at_least < occurences:
                    self.yellow[actual_colors["yellow"][i]].at_least = occurences
                self.yellow[actual_colors["yellow"][i]].indexes[i] = 1

            if actual_colors["gray"][i] in ascii_lowercase:
                self.gray[actual_colors["gray"][i]].at_least = 1
                self.gray[actual_colors["gray"][i]].indexes[i] = 1

    @timer
    def create_testing_colors(self):
        new = {
            "green": ["0"] * 5,
            "yellow": ["0"] * 5,
            "gray": ["0"] * 5
        }
        return new
