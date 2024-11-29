import argparse
import time

from xordle import XordleSolver, XordleEmulator, Status


def main(games):
    bad = 0
    not_guessed = ["xclue word1 word2\n"]
    all_games = ["xclue word1 word2\n"]

    for index in range(1, games + 1):
        emulator = XordleEmulator()
        solver = XordleSolver()

        clue_word, color = emulator.start()

        current_game = f"{clue_word} {emulator.emulator_word1} {emulator.emulator_word2}"
        all_games.append(current_game)

        solver.load_initial_word(clue_word)

        lock_count = 0
        while not (emulator.status & Status.FINISHED):
            try:
                guessed_word = solver.load_color(color, emulator.huh)
                color = emulator.guess(guessed_word)

                lock_count += 1
                if lock_count > 15:
                    raise Exception()
            except Exception:
                bad += 1
                not_guessed.append(current_game)
                print("ERROR/DEADLOCK " + current_game)
                break

        if emulator.status != Status.WIN:
            bad += 1
            not_guessed.append(current_game)
            print("NOT GUESSED " + current_game)

        if index % 10 == 0:
            accuracy = (index - bad) / index * 100
            print(f"Current accuracy: ({accuracy:.2f}% {index - bad}/{index})")

    accuracy = (games - bad) / games * 100
    result = f"Total accuracy: {accuracy:.2f}% ({games - bad}/{games})"
    return not_guessed, all_games, result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--games',
        type=int,
        default=100,
    )
    args = parser.parse_args()

    if args.games <= 0:
        raise ValueError("--games should be a number greater than 0")
    else:
        start = time.time()
        not_guessed, all_games, result = main(args.games)
        print(f"\nTest took: {time.time() - start:.4f} seconds")
        print(result)

        with open("log/not_guessed.txt", "w") as f:
            f.write("\n".join(not_guessed))

        with open("log/all_games.txt", "w") as f:
            f.write("\n".join(all_games))
