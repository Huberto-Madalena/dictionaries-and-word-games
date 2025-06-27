import pandas as pd
import nltk
import json
import os
from nltk.corpus import wordnet
from nltk import download

# WordNet available
def wordnet_available():
    try:
        wordnet.synsets("test")
    except LookupError:
        print("couldn\'t find WordNet. download in progress")
        download("wordnet")

wordnet_available()

# json file keeps the dictionary
DICT_FILE = "data_fen.json"

# Load default dictionary
if os.path.exists(DICT_FILE):
    with open(DICT_FILE, "r") as f:
        data_fen = json.load(f)
else:
    data_fen = {
        "angry": ["grouchy", "grumpy", "cranky", "recalcitrant"],
        "gaudy": ["garish", "flamboyant", "flashy", "showy"]
    }

# Get synonyms from WordNet
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.name().lower() != word.lower():
                synonyms.add(lemma.name().replace("_", " "))
    return list(synonyms)

# it shows the last 5 entries
def show_last_entries(dictionary, count=5):
    last_5_items = dict(list(dictionary.items())[-5:])
    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in last_5_items.items()]))
    print("\nLast entries in the dictionary:")
    print(df)

# Save to a file, using the argument 'w' for write
def save_dictionary(dictionary):
    with open(DICT_FILE, "w") as f:
        json.dump(dictionary, f, indent=2)

# menu wrapped in a loop
while True:
    print("\n--- Dictionary ---")
    print("1. Look up a definition")
    print("2. Insert a new word")
    print("0. Exit")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        word = input("Enter a word to look up: ").strip().lower()
        if word in data_fen:
            print(f"\nSynonyms for '{word}': {data_fen[word]}")
        else:
            print(f"'{word}' not found.")
    
    elif choice == "2":
        new_word = input("Enter a word to add: ").strip().lower()
        if new_word in data_fen:
            print(f"'{new_word}' already exists with synonyms: {data_fen[new_word]}")
        else:
            synonyms = get_synonyms(new_word)
            if synonyms:
                data_fen[new_word] = synonyms[:5]
                save_dictionary(data_fen)
                print(f"Added '{new_word}' with synonyms: {data_fen[new_word]}")
                show_last_entries(data_fen)
            else:
                print(f"No synonyms found for '{new_word}'. this word '{new_word}' is not being added.")
    
    elif choice == "0":
        print("leaving.....")
        break
    else:
        print("that\'s a weird option. Please choose 1, 2, or 0.")
