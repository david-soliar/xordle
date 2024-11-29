import sys
import traceback

from xordle import XordleSolver, XordleEmulator, Status


def parse_arguments():
    if len(sys.argv) != 4:
        raise ValueError("Usage: demo05.py <clue_word> <word1> <word2>")

    clue_word = sys.argv[1]
    words = (sys.argv[2], sys.argv[3])

    if len(clue_word) != 5 or len(words[0]) != 5 or len(words[1]) != 5:
        raise ValueError("All words must be 5 characters long.")

    return clue_word, words


def main():
    clue_word, words = parse_arguments()

    emulator = XordleEmulator(words=words, clue_word=clue_word, enable_logging=True)
    solver = XordleSolver(enable_logging=True)

    clue_word, color = emulator.start()

    print("Initial color:", color)
    print("Initial HUH:", emulator.huh)

    solver.load_initial_word(clue_word)

    lock_count = 0
    while not (emulator.status & Status.FINISHED):
        try:
            word = solver.load_color(color, emulator.huh)
            color = emulator.guess(word)

            lock_count += 1
            if lock_count > 15:
                raise Exception()
        except Exception:
            print(f"ERROR/DEADLOCK: {word} {color} {emulator.huh} {emulator.status} {solver.status} {solver.xordle_player.top}")
            traceback.print_exc()
            return

    if color:
        solver.load_color(color, emulator.huh)

    if emulator.status != Status.WIN:
        print(f"YOU LOST: {word} {color} {emulator.huh}")
        rank_shit = ((solver.xordle_player.word_exists_test(words[0]) and solver.xordle_player.word_exists_test(words[1]))
                     or (solver.xordle_player.word_exists_test(words[0]) and solver.guessed == 1)
                     or (solver.xordle_player.word_exists_test(words[1]) and solver.guessed == 1))
        if rank_shit:
            print(f"SHIT RANKING, guessed: {solver.guessed}")
        return

    print("ALL GOOD")


if __name__ == "__main__":
    main()
