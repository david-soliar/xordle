import time

from xordle import XordleSolver, XordleEmulator, Status


def main(all_data):
    bad = 0

    print("TYPE xclue word1 word2 emulator.STATUS\n")

    for line in all_data:
        line = line.split()
        emulator = XordleEmulator(clue_word=line[0], words=line[1:])
        solver = XordleSolver()

        clue_word, color = emulator.start()

        current_game = f"{clue_word} {emulator.emulator_word1} {emulator.emulator_word2}"

        solver.load_initial_word(clue_word)

        lock_count = 0
        while not (emulator.status & Status.FINISHED):
            try:
                word = solver.load_color(color, emulator.huh)
                color = emulator.guess(word)

                lock_count += 1
                if lock_count > 15:
                    raise Exception
            except Exception:
                print(f"ERROR/DEADLOCK {current_game} {emulator.status}")
                break

        if emulator.status != Status.WIN:
            bad += 1
            print(f"NOT GUESSED {current_game} {emulator.status}")

        else:
            print(f"GOOD {current_game} {emulator.status}")

    return bad


if __name__ == "__main__":
    try:
        with open("log/not_guessed.txt", "r") as f:
            all_data = f.readlines()[2:]

        start = time.time()
        bad = main(all_data)
        print(f"\nTest took: {time.time() - start:.2f} seconds")
        print(f"Total accuracy: {len(all_data) - bad}/{len(all_data)}")

    except FileNotFoundError:
        print("The file log/not_guessed.txt was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
