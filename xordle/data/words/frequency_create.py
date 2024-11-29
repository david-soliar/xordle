import pathlib
import string
import json


current_dir = pathlib.Path(__file__).parent

with current_dir.joinpath("xordle.txt").open(mode="r") as file:
    data = file.read().split()

character_freq = dict()

for char in string.ascii_lowercase:
    character_freq[char] = 0

for word in data:
    for char in word:
        character_freq[char] += 1

with current_dir.joinpath("xordle.frequency").open(mode="w") as file:
    json.dump(character_freq, file, indent=4)

sum = 0
for key in character_freq.keys():
    sum += character_freq[key]

if sum == len(data)*5:
    print("GOOD")
