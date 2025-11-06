from collections import Counter
from string import ascii_lowercase

from .data.data import Data
from .data.timer import timer


class Ranking(Data):
    def __init__(self, enable_logging):
        super().__init__(enable_logging=enable_logging)
        self.when_excluded_ranking = None

    @timer
    def green_guess(self):
        for i in range(5):
            green_char1_sum = 0
            green_char2_sum = 0

            green_char1_index = -1
            green_char2_index = -1

            index = 0
            while index <= self.top:
                if self.green1[i] != "" and self.green1[i] == self.words[index].word[i]:
                    green_char1_sum += 1
                    green_char1_index = index

                if self.green2[i] != "" and self.green2[i] == self.words[index].word[i]:
                    green_char2_sum += 1
                    green_char2_index = index

                index += 1

            if green_char1_sum == 1:
                self.logger.log_print("GREEN_GUESS GUESSED ?")
                return green_char1_index
            if green_char2_sum == 1:
                self.logger.log_print("GREEN_GUESS GUESSED ?")
                return green_char2_index

        return -1

    @timer
    def index_of_word_containing_char_on_index(self, i, char):
        index = 0
        while index <= self.top:
            if self.words[index].word[i] == char:
                return index
            index += 1

    @timer
    def index_of_word(self, word_e):
        index = 0
        while index <= self.top:
            if self.words[index].word == word_e:
                return index
            index += 1

    @timer
    def count_of_words_containing_char_on_index(self, i, char):
        count = 0
        index = 0
        while index <= self.top:
            if self.words[index].word[i] == char:
                count += 1
            index += 1
        return count

    @timer
    def only_special_word_index(self):
        characters_on_index = [list(), list(), list(), list(), list()]

        index = 0
        while index <= self.top:
            for i in range(5):
                characters_on_index[i].append(self.words[index].word[i])
            index += 1

        for i in range(5):
            setx = list(set(characters_on_index[i]))
            if len(setx) == 2:
                if self.count_of_words_containing_char_on_index(i, setx[0]) == 1:
                    self.logger.log_print("SPECIAL WORD")
                    return self.index_of_word_containing_char_on_index(i, setx[0])
                if self.count_of_words_containing_char_on_index(i, setx[1]) == 1:
                    self.logger.log_print("SPECIAL WORD")
                    return self.index_of_word_containing_char_on_index(i, setx[1])
        return -1

    @timer
    def guess_word_index(self, guess_count, guessed):
        super_index = -1
        if guessed == 0 and (guess_count == 5 or guess_count == 6):
            super_index = self.only_special_word_index()

        if ((guess_count == 5 or guess_count == 6)
                and ((guessed == 1 and self.top > 0 and self.top < 10) or (guessed == 0 and super_index != -1))):
            deciding_word_index = self.find_deciding_word_index(super_index)
            if deciding_word_index != -1:
                return deciding_word_index

        if super_index != -1:
            return super_index

        if (guess_count > 2 and guess_count < 5) or guess_count == 7:
            green_guess_index = self.green_guess()
            if green_guess_index != -1:
                return green_guess_index

        if guess_count == 6 and self.top > 20:
            return self.find_deciding_word_index(super_index, brute_force=True)

        if guessed == 0 and guess_count == 6 and self.top > 1 and self.top < 10 and self.when_excluded_ranking:
            exclude_this = Counter(self.when_excluded_ranking).most_common(1)[0][0]
            self.logger.log_print("EXCLUDED LIST")
            return self.index_of_word(exclude_this)

        max_probability = -100
        min_probability = 100

        good_return_this = 0
        bad_return_this = 0

        frequency_of_characters = [item[0] for item in sorted(self.character_frequency.items(), key=lambda item: item[1], reverse=True)]

        early_guess = guess_count < 5

        index = 0
        while index <= self.top:
            probability = 0

            for i in range(5):
                if (self.words[index].word[i] == self.green1[i]
                        or self.words[index].word[i] == self.green2[i]):
                    probability += 3

            if early_guess and self.words[index].unique_characters != 5:
                probability += 3

            if early_guess:
                for char in self.words[index].word:
                    if self.gray[char].at_least == 0:
                        probability -= 2

            if early_guess:
                for character in set(self.words[index].word):
                    if character not in self.green1 and character not in self.green2:
                        probability -= (26 - frequency_of_characters.index(character))/26

            for character in ascii_lowercase:
                if self.yellow[character].at_least > 0:
                    in_word = self.words[index].word.count(character)
                    if in_word == (self.yellow[character].at_least
                                   + self.green1.count(character)
                                   + self.green2.count(character)):
                        if early_guess and guess_count > 3:
                            probability -= 2
                        else:
                            probability += 1
                    elif in_word > (self.yellow[character].at_least
                                    + self.green1.count(character)
                                    + self.green2.count(character)):
                        if early_guess and guess_count > 3:
                            probability -= 1
                        else:
                            probability += 1
                    if early_guess:  # tu teoreitcky  and in_word > 0
                        for i in range(5):
                            if self.yellow[character].indexes[i] == 0:
                                probability -= 0.5

            if probability > max_probability:
                max_probability = probability
                good_return_this = index

            if (probability == max_probability and self.words[index].api_frequency > self.words[good_return_this].api_frequency):
                good_return_this = index

            if probability < min_probability and self.words[index].unique_characters == 5:
                min_probability = probability
                bad_return_this = index

            if self.top < 500:
                self.logger.log_print(f"{self.words[index].word},  prob: {probability}, api:{self.words[index].api_frequency}")

            index += 1

        self.logger.log_print(f"\nEARLY GUESS RANKING: {early_guess}")
        if early_guess:
            return bad_return_this
        return good_return_this

    @timer
    def find_deciding_word_index(self, special_word_index, brute_force=False):
        characters_on_index = [list(), list(), list(), list(), list()]

        index = 0
        while index <= self.top:
            if index != special_word_index:
                for i in range(5):
                    characters_on_index[i].append(self.words[index].word[i])
            index += 1

        chars_good_count = 5
        characters_to_find = set()
        more_chars = 0
        for char_set_index in range(5):
            setx = set(characters_on_index[char_set_index])

            if len(setx) == 1:
                characters_on_index[char_set_index] = list()
                chars_good_count -= 1
            else:
                more_chars += 1
                characters_to_find = setx

        if chars_good_count < 3 and (more_chars < 3 or brute_force):
            max_find = 0
            return_index = -1

            if brute_force:
                exclude = set([x for x in self.green1 if x]) | set([x for x in self.green2 if x])
                characters_to_find = {key: value for key, value in self.character_frequency.items()}
                for e in exclude:
                    del characters_to_find[e]
                characters_to_find = sorted(characters_to_find, key=lambda k: characters_to_find[k])

                index = 0
                while index <= self.top:
                    find = 0
                    for char in self.words[index].word:
                        if char in characters_to_find:
                            find += (characters_to_find.index(char) ** (3/2))
                    if find > max_find:
                        max_find = find
                        return_index = index
                    index += 1
                self.logger.log_print("DECIDING RANKING BRUTE FORCE FOUND")
                return return_index

            index = 0
            while index <= self.total_top:
                find = len(set(self.words[index].word) & characters_to_find)
                if find > max_find:
                    max_find = find
                    return_index = index
                index += 1
            self.logger.log_print("DECIDING RANKING FOUND")
            return return_index

        return -1
