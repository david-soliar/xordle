from .player import player
from .status import Status


class XordleSolver():
    def __init__(self, enable_logging=False):
        self.xordle_player = player(enable_logging=enable_logging)

        self.guessed = 0
        self.guess_count = 0

        self.index_of_guessed_word = -1
        self.word = None
        self.bonus = False

        self.status = Status.IN_PROGRESS

        self.already_guessed = list()
        self.already_guessed_colors = list()

    def load_initial_word(self, word):
        self.word = word
        self.already_guessed.append(self.word)

    def load_color(self, color, huh):
        if self.guess_count > 8 or self.status != Status.IN_PROGRESS:
            return None

        if (self.guess_count == 8) and color != "22222":
            self.status = Status.LOSS
            self.already_guessed_colors.append(color)
            self.xordle_player.logger.log_print("LOSS"*10)
            self.xordle_player.log_exec_time()
            self.xordle_player.process_guess(self.word, color, self.guess_count, self.guessed, self.index_of_guessed_word)
            return None

        if color == "22222":
            if not huh and self.guessed == 1:
                self.status = Status.WIN
                self.already_guessed_colors.append(color)
                self.xordle_player.logger.log_print("WIN"*10)
                self.xordle_player.log_exec_time()
                return None

            elif not huh:
                self.guessed += 1
                self.xordle_player.clean_after_good_guess(self.word, self.guessed)

                #bonus
                if self.guess_count == 8:
                    self.guess_count -= 1
                    self.bonus = True
                    self.xordle_player.logger.log_print("BONUS")

            else:
                self.xordle_player.logger.log_print("HUH")
                if self.guess_count == 8:
                    self.status = Status.LOSS
                    self.already_guessed_colors.append(color)
                    self.xordle_player.logger.log_print("LOSS"*10)
                    self.xordle_player.log_exec_time()
                    self.xordle_player.process_guess(self.word, color, self.guess_count, self.guessed, self.index_of_guessed_word)
                    return None
                else:
                    self.xordle_player.process_guess(self.word, color, self.guess_count, self.guessed, self.index_of_guessed_word)

            self.index_of_guessed_word = self.xordle_player.guess_word_index(self.guess_count, self.guessed)
            self.word = self.xordle_player.words[self.index_of_guessed_word].word
            self.already_guessed.append(self.word)
            self.already_guessed_colors.append(color)

            self.guess_count += 1
            self.xordle_player.logger.log_print("Next word: " + self.word)
            return self.word

        self.xordle_player.process_guess(self.word, color, self.guess_count, self.guessed, self.index_of_guessed_word)
    
        self.index_of_guessed_word = self.xordle_player.guess_word_index(self.guess_count, self.guessed)
        self.word = self.xordle_player.words[self.index_of_guessed_word].word
        self.already_guessed.append(self.word)
        self.already_guessed_colors.append(color)

        self.guess_count += 1
        self.xordle_player.logger.log_print("Next word: " + self.word)
        return self.word

    @staticmethod
    def cli(hard=False):
        if hard:
            return XordleSolver._hard_mode()
        return XordleSolver._normal_mode()

    @staticmethod
    def _normal_mode():
        xordle_player = player()
        print("XORDLE - normal mode CLI\n")

        word = input("Enter revealed word: ")

        guessed = 0
        guess_count = 0

        index_of_guessed_word = -1
        while guess_count < 9:
            while True:
                color = input("Enter color in format 00000: ")
                if len(color) == 5 and all(c in "012" for c in color):
                    break
                print("*Invalid color, please try again*")

            if (guess_count == 8) and color != "22222":
                print("YOU LOST!")
                return

            if color == "22222":
                while True:
                    huh = input("Huh? Did huh? appear next to your answer? (y/n): ")
                    if huh == "y" or huh == "n":
                        break
                    print("*Use y for YES or n for NO, please try again*")

                if huh == "n" and guessed == 1:
                    print("YOU WIN!")
                    return

                elif huh == "n":
                    guessed += 1
                    xordle_player.clean_after_good_guess(word, guessed)

                    #bonus
                    if guess_count == 8:
                        guess_count -= 1

                else:
                    if guess_count == 8:
                        print("YOU LOST!")
                        return
                    else:
                        xordle_player.process_guess(word, color, guess_count, guessed, index_of_guessed_word)

                index_of_guessed_word = xordle_player.guess_word_index(guess_count, guessed)
                word = xordle_player.words[index_of_guessed_word].word
                guess_count += 1
                print("Next word: ", word)

                continue

            xordle_player.process_guess(word, color, guess_count, guessed, index_of_guessed_word)

            index_of_guessed_word = xordle_player.guess_word_index(guess_count, guessed)
            word = xordle_player.words[index_of_guessed_word].word
            guess_count += 1
            print("Next word: ", word)

    @staticmethod
    def _hard_mode():
        xordle_player = player()
        print("XORDLE - hard mode CLI\n")

        guessed = 0
        guess_count = 0

        index_of_guessed_word = xordle_player.guess_word_index(guess_count, guessed)
        word = xordle_player.words[index_of_guessed_word].word
        print("Next word: ", word)

        while guess_count < 9:
            if guess_count >= 0 and guess_count <= 4:
                while True:
                    character = input("Enter new revealed character: ")
                    if len(character) == 1:
                        break
                    print("*Enter exactly ONE character, please try again*")
                while True:
                    char_color = input("Enter color of new character (0 or 1 or 2): ")
                    if len(char_color) == 1 and char_color in "012":
                        break
                    print("*Invalid color, please try again*")

                imaginary_word = list(".....")
                imaginary_word[guess_count] = character
                imaginary_color = list("00000")
                imaginary_color[guess_count] = char_color
                xordle_player.process_guess("".join(imaginary_word),
                                            "".join(imaginary_color),
                                            guess_count, guessed, -1)

            while True:
                color = input("Enter color of word in format 00000: ")
                if len(color) == 5 and all(c in "012" for c in color):
                    break
                print("*Invalid color, please try again*")

            if (guess_count == 8) and color != "22222":
                print("YOU LOST!")
                return

            if color == "22222":
                while True:
                    huh = input("Huh? Did huh? appear next to your answer? (y/n): ")
                    if huh == "y" or huh == "n":
                        break
                    print("*Use y for YES or n for NO, please try again*")

                if huh == "n" and guessed == 1:
                    print("YOU WIN!")
                    return

                elif huh == "n":
                    guessed += 1
                    xordle_player.clean_after_good_guess(word, guessed)

                    #bonus
                    if guess_count == 8:
                        guess_count -= 1

                else:
                    if guess_count == 8:
                        print("YOU LOST!")
                        return
                    else:
                        xordle_player.process_guess(word, color, guess_count, guessed, index_of_guessed_word)

                index_of_guessed_word = xordle_player.guess_word_index(guess_count, guessed)
                word = xordle_player.words[index_of_guessed_word].word
                guess_count += 1
                print("Next word: ", word)

                continue

            xordle_player.process_guess(word, color, guess_count, guessed, index_of_guessed_word)
            index_of_guessed_word = xordle_player.guess_word_index(guess_count, guessed)
            word = xordle_player.words[index_of_guessed_word].word
            guess_count += 1

            print("Next word: ", word)
