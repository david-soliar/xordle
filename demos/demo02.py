import argparse
import time

from xordle import XordleSolver, XordleEmulator, Status


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--offset',
        type=int,
        default=0
    )
    parser.add_argument(
        '--games',
        type=int,
        default=1000
    )
    return parser.parse_args()


def main(all_data, offset, games):
    bad = 0
    print("MESSAGE xclue word1 word2\n")

    for index, line in enumerate(all_data[offset:offset + games], start=1):
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
                    raise Exception()
            except Exception:
                bad += 1
                print("ERROR/DEADLOCK " + current_game)
                break

        if emulator.status != Status.WIN:
            bad += 1
            print("NOT GUESSED " + current_game)

        if index % 10 == 0:
            accuracy = (index - bad) / index * 100
            print(f"Current accuracy: {accuracy:.2f}% ({index - bad}/{index})")

    accuracy = (games - bad) / games * 100
    result = f"Total accuracy: {accuracy:.2f}% ({games - bad}/{games})"
    return result


if __name__ == "__main__":
    args = parse_arguments()

    with open("xordle.org.txt", "r") as file:
        all_data = file.readlines()
    
    if args.games <= 0 or args.offset < 0:
        raise ValueError("arguments should be numbers greater than or equal to 0")

    else:
        start_time = time.time()
        result = main(all_data, args.offset, args.games)
        print(f"\nTest took: {time.time() - start_time:.2f} seconds")
        print(result)
