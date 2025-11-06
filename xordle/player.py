import copy
import time
from string import ascii_lowercase

from .ranking import Ranking
from .color_filter import ColorFilter
from .words_filter import WordsFilter
from .data.timer import timer, get_timer


class player(Ranking, WordsFilter, ColorFilter):
    def __init__(self, enable_logging=True):
        super().__init__(enable_logging=enable_logging)
        self.logger.log_print("PLAYER START")

    def log_exec_time(self):
        sorted_dict = dict(sorted(get_timer().items(), key=lambda item: item[1], reverse=True))
        self.logger.log_print(str(sorted_dict).replace(",", ",\n"))

    @timer
    def process_guess(self, word, color, guess_count, guessed, index_of_previous_guess):
        if index_of_previous_guess == -1 and color == "22222":
            self.remove_guessed_word(word)
        else:
            self.remove_word_on_index(index_of_previous_guess)

        actual_colors = self.create_testing_colors()

        for i in range(5):
            if color[i] == "2" and (word[i] in ascii_lowercase):
                actual_colors["green"][i] = word[i]
            if color[i] == "1" and (word[i] in ascii_lowercase):
                actual_colors["yellow"][i] = word[i]

        for i in range(5):
            if (color[i] == "0" and (word[i] in ascii_lowercase)
                    and (word[i] not in actual_colors["green"])
                    and (word[i] not in actual_colors["yellow"])
                    and (word[i] not in actual_colors["gray"])):
                actual_colors["gray"][i] = word[i]

        for i in range(5):
            if color[i] == "0" and word[i] in actual_colors["green"]:
                self.remove_words_that_contain_gray_and_green_or_yellow_at_the_same_time_but_on_different_index(actual_colors["green"], actual_colors["yellow"], word[i])

        for i in range(5):
            if color[i] == "0" and (word[i] in actual_colors["yellow"] or word[i] in actual_colors["green"]):
                self.remove_word_that_has_gray_and_also_same_green_or_yellow(actual_colors["green"], actual_colors["yellow"], word[i])

        self.update_colors(actual_colors, word, color)

        green_sum, yellow_sum, gray_sum = self.remake_actual_colors_and_sum_it(actual_colors)

        if gray_sum > 0:
            self.remove_words_containing_gray(actual_colors["gray"])

        if yellow_sum > 0:
            self.remove_words_containing_yellow_on_index(actual_colors["yellow"])

        if yellow_sum + gray_sum > 0:
            self.infer_green_by_gray_and_yellow()

        if green_sum > 0:
            self.update_green_color(actual_colors["green"])

        self.remove_found_yellow_by_green_position()

        self.infer_green_by_yellow_position()
        self.infer_green_by_gray_and_yellow()

        if guessed != 0:
            self.remove_word_if_not_all_yellow_after_clean()

        self.remove_found_yellow_by_green_position()
        self.remove_words_if_yellow_green_full()

        if guess_count >= 5:
            for i in range(5):
                self.remove_words_with_green_missmatch(i, guessed)
            self.remove_words_with_green_characters_on_wrong_index()

        if guessed == 0 and guess_count >= 3:
            self.when_excluded_ranking = self.remove_words_that_when_excluded_destory_list_of_words()

        self.logger.log_green(self.green1, self.green2)
        self.logger.log_color(self.yellow, "yellow")
        self.logger.log_color(self.gray, "gray")
        self.logger.log_print(f"CURRENT GUESS: {guess_count}, WORD BEING PROCESSED: {word}, COLOR IS: {color}")
        self.logger.log_words(self.words, self.top, all=self.top < 100)

    @timer
    def clean_after_good_guess(self, word, guessed, test=False):
        if not test:
            self.logger.log_print("CLEAN GUESSED - JEDNO SLOVO UHADNUTE")

        self.remove_words_containing_gray(word)

        for i in range(5):
            self.gray[word[i]].indexes[i] = 1
            self.yellow[word[i]].indexes = [0, 0, 0, 0, 0]
            self.yellow[word[i]].at_least = 0

            if self.green1[i] == word[i]:
                self.green1[i] = ""
            elif self.green2[i] == word[i]:
                self.green2[i] = ""

        self.remove_word_if_not_all_yellow_after_clean()

        self.infer_green_by_yellow_position()
        self.infer_green_by_gray_and_yellow()

        for i in range(5):
            self.remove_words_with_green_missmatch(i, guessed)
        self.remove_words_with_green_characters_on_wrong_index()

        if not test:
            self.logger.log_green(self.green1, self.green2)
            self.logger.log_color(self.yellow, "yellow")
            self.logger.log_color(self.gray, "gray")
            self.logger.log_words(self.words, self.top, all=self.top < 100)

    @timer
    def fill_imaginary_player(self, imaginary_player):
        imaginary_player.words = copy.copy(self.words)
        imaginary_player.character_frequency = copy.deepcopy(self.character_frequency)
        imaginary_player.top = self.top
        imaginary_player.yellow = copy.deepcopy(self.yellow)
        imaginary_player.gray = copy.deepcopy(self.gray)
        imaginary_player.green1 = copy.deepcopy(self.green1)
        imaginary_player.green2 = copy.deepcopy(self.green2)

    @timer
    def remove_words_that_when_excluded_destory_list_of_words(self):
        imaginary_player = player(enable_logging=False)
        initial_top = self.top
        when_excluded = list()

        index = 0
        while index <= self.top:
            removedp = False

            self.fill_imaginary_player(imaginary_player)

            imaginary_player.clean_after_good_guess(self.words[index].word, 1, test=True)
            if imaginary_player.top < 0:
                self.remove_word_on_index(index)
                removedp = True

            else:
                for i in range(imaginary_player.top + 1):
                    when_excluded.append(imaginary_player.words[i].word)

            if not removedp:
                index += 1

        self.logger.log_print(f"remove_words_that_when_excluded_destory_list_of_words")
        if self.top < initial_top:
            self.logger.log_print(f"remove_words_that_when_excluded_destory_list_of_words REMOVED {initial_top - self.top}")
            return self.remove_words_that_when_excluded_destory_list_of_words()
        return when_excluded

    @timer
    def word_exists_test(self, word):
        index = 0
        while index <= self.top:
            if self.words[index].word == word:
                return True
            index += 1
        return False
