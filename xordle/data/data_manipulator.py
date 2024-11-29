import pathlib
import pickle
import json
from collections import namedtuple


word_data = namedtuple('word_data', ['word', 'unique_characters', 'api_frequency'])


def create(current_dir):
    with current_dir.joinpath("words", "words.txt").open(mode="r") as file:
        data = file.read().split()

    with current_dir.joinpath("words", "words.json").open(mode="r") as words_json:
        json_data = json.load(words_json)

    words = list()
    for word in data:
        words.append(word_data(word=word, unique_characters=len(set(word)), api_frequency=json_data[word]))

    with current_dir.joinpath("data.pkl").open(mode="wb") as file:
        pickle.dump(words, file)


def load_words():
    current_dir = pathlib.Path(__file__).parent

    try:
        with current_dir.joinpath("data.pkl").open(mode="rb") as file:
            data = pickle.load(file)
    except Exception:
        create(current_dir)
        with current_dir.joinpath("data.pkl").open(mode="rb") as file:
            data = pickle.load(file)

    return data


def load_character_frequency():
    current_dir = pathlib.Path(__file__).parent

    with current_dir.joinpath("words", "words_characters.frequency").open(mode="r") as file:
        character_frequency = json.load(file)

    return character_frequency
