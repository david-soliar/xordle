# xordle

xordle is a Python package that provides tools to solve and interact with the Xordle word-guessing game. The module includes the core solver logic, a simplified emulator for testing, and CLI modes for interaction. It is designed to help analyze the game and automate the guessing process.

## Installation

To install xordle locally for testing and development, use the following command in your terminal
(make sure you're in the root of the project directory):

```bash
pip install -e .
```

## Running Demos

Once the module is installed, you can test different functionalities using the demo scripts in the `demos` folder. 


### Make sure you’re in the root directory when running demos

### 1. `demo01.py` - Testing 100 attempts and success Rate

#### This uses the Emulator, which is more challenging than the real xordle.org games. For a more accurate test, use `demo02.py`.
This demo runs a default of 100 attempts (but you can specify a different number) and logs the success rate of solving the Xordle puzzle.

When scripts finishes 2 files will appear:
- `/log/not_guessed.txt` containing games, which solver could not guess
- `/log/all_games.txt` containing all games

#### How to Run:

- By default, the script will run 100 attempts. To run it with a different number of attempts, use the `--games` argument followed by the desired number.

    ```bash
    python demos/demo01.py --games 999
    ```

- If no argument is passed, it will default to 100 attempts.

    ```bash
    python demos/demo01.py
    ```

### 2. `demo02.py` - Testing first 1000 games from xordle.org

#### This uses real xordle.org games. For more broad testing, use `demo01.py`.
This demo runs a configurable number of attempts (default is 1000) and logs the success rate of solving the Xordle puzzle.

#### How to Run:

- By default, the script will run 1000 attempts starting from the first game. You can modify the number of games to test and the offset using the `--offset` and `--games` arguments.

    To run the demo with the default settings (1000 games starting from the first):

    ```bash
    python demos/demo02.py
    ```

- To specify a different starting game or the number of games to test, use the `--offset` (starting game) and `--games` (number of games) options:

    Example with offset and custom number of games:

    ```bash
    python demos/demo02.py --offset 100 --first_n_games 500
    ```

### 4. `demo03.py` - Running xorlde solver in CLI Normal Mode
This demo runs the solver in CLI mode, where you can play the Xordle in normal mode version.

#### How to Run:

- Run the following command:

    ```bash
    python demos/demo03.py
    ```

### 3. `demo04.py` - Running xordle solver in CLI Hard Mode
This demo runs the solver in CLI mode, where you can play the Xordle in hard mode version.

#### How to Run:

- Run the following command:

    ```bash
    python demos/demo04.py
    ```

### 5. `demo05.py` - Testing one attempt with given clue and two words to guess
This demo is similar to `demo01.py` but only tests a single attempt with a given first word and two guessed words.

#### How to Run:

- Run the following command:

    ```bash
    python demos/demo05.py xclue word1 word2
    ```
*(xclue word1 word2) are words of your choice

### 5. `demo06.py` - Testing all games which solver in `demo01.py` failed to guess
This demo tests all games in file `/log/not_guessed.txt` generated by `demo01.py`.

#### How to Run:

- Run the following command:

    ```bash
    python demos/demo06.py
    ```

# TODO - Currently, the Emulator supports only normal mode. Add hard mode
# TODO - HUH LOCK - extra filter when there are too much huhs
# TODO - rework this whole project, + pep8, + docs, + optimize
