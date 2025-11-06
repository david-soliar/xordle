from string import ascii_lowercase

from .data.data import Data
from .data.timer import timer


class WordsFilter(Data):
    def __init__(self, enable_logging):
        super().__init__(enable_logging=enable_logging)

    @timer
    def remove_guessed_word(self, word):
        index = 0
        while index <= self.top:
            if self.words[index].word == word:
                self.remove_word_on_index(index)
                return
            index += 1

    @timer
    def remove_words_with_green_characters_on_wrong_index(self):
        index = 0
        while index <= self.top:
            removedp = False

            for i in range(5):
                if (self.green1[i] != ""
                        and self.green1[i] in self.words[index].word
                        and self.green1[i] != self.words[index].word[i]):
                    self.remove_word_on_index(index)
                    removedp = True
                    break
                elif (self.green2[i] != ""
                        and self.green2[i] in self.words[index].word
                        and self.green2[i] != self.words[index].word[i]):
                    self.remove_word_on_index(index)
                    removedp = True
                    break

            if not removedp:
                index += 1

    @timer
    def remove_words_with_green_missmatch(self, i, guessed):
        if guessed == 0 and (self.green1[i] == "" or self.green2[i] == ""):
            return

        if guessed == 1 and (self.green1[i] == "" and self.green2[i] == ""):
            return

        index = 0
        while index <= self.top:
            if guessed == 1:
                if (self.words[index].word[i] != self.green1[i]
                        and self.words[index].word[i] != self.green2[i]):
                    self.remove_word_on_index(index)
                else:
                    index += 1
            elif guessed == 0:
                if (self.words[index].word[i] == self.green1[i]
                        or self.words[index].word[i] == self.green2[i]):
                    index += 1
                else:
                    self.remove_word_on_index(index)

    @timer
    def remove_words_if_yellow_green_full(self):
        sum = 0
        found_characters = list()
        for character in ascii_lowercase:
            if self.yellow[character].at_least > 0:
                sum += self.yellow[character].at_least
                found_characters.append(character)

        for i in range(5):
            if self.green1[i]:
                found_characters.append(self.green1[i])
                sum += 1

            if self.green2[i]:
                found_characters.append(self.green2[i])
                sum += 1

        if sum == 10:
            characters_to_remove = set(ascii_lowercase) - set(found_characters)
            self.remove_words_containing_gray(characters_to_remove)

    @timer
    def remove_word_if_not_all_yellow_after_clean(self):
        index = 0
        while index <= self.top:
            removedp = False
            for character in ascii_lowercase:
                if (self.yellow[character].at_least != 0
                        and (character not in self.words[index].word)):
                    self.remove_word_on_index(index)
                    removedp = True
                    break
            if not removedp:
                index += 1

    @timer
    def remove_words_containing_yellow_on_index(self, yellow_characters):
        index = 0
        while index <= self.top:
            removedp = False

            for i in range(5):
                if (self.words[index].word[i] == yellow_characters[i]):
                    self.remove_word_on_index(index)
                    removedp = True
                    break

            if not removedp:
                index += 1

    @timer
    def remove_words_containing_gray(self, gray_characters):
        grays = set("".join(gray_characters))

        index = 0
        while index <= self.top:
            removedp = False
            if grays & set(self.words[index].word):
                self.remove_word_on_index(index)
                removedp = True

            if not removedp:
                index += 1

    @timer
    def remove_word_that_has_gray_and_also_same_green_or_yellow(self, actual_green, actual_yellow, gray_character):
        count = actual_green.count(gray_character) + actual_yellow.count(gray_character)

        index = 0
        while index <= self.top:
            if gray_character not in self.words[index].word:
                index += 1
                continue

            actual_word_count = self.words[index].word.count(gray_character)
            if count != actual_word_count:
                self.remove_word_on_index(index)
            else:
                index += 1

    @timer
    def remove_words_that_contain_gray_and_green_or_yellow_at_the_same_time_but_on_different_index(self, actual_green, actual_yellow, gray_character):
        index = 0
        while index <= self.top:
            if gray_character not in self.words[index].word:
                index += 1
                continue

            removedp = False
            for i in range(5):
                if (self.words[index].word[i] == gray_character
                        and actual_green[i] != gray_character
                        and gray_character not in actual_yellow):
                    self.remove_word_on_index(index)
                    removedp = True
                    break
            if not removedp:
                index += 1

    @timer
    def remove_word_on_index(self, index):
        if (index < 0 or index > self.top):
            self.logger.log_print("Index out of range: remove_word_on_index")
            return

        for character in self.words[index].word:
            self.character_frequency[character] -= 1

        self.words[index], self.words[self.top] = self.words[self.top], self.words[index]
        self.top -= 1
