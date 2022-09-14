import random

import requests

def readData():
    english_word_url = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
    english_Word_url = "https://github.com/Abdullahi-a-hussein/typing-speed-app/raw/master/words.txt"
    print(f"Retrieving English Word from {english_word_url} ... ")
    response = requests.get(english_word_url)
    words = []
    word=""
    for line in response.text:
        if line != '\n':
            word += line
        else:
            words.append(word.lower().strip())
            word = ""
    print(f"Retrieved {len(words)} English Words")
    random.shuffle(words)
    return words

def readLocalData():
    with open("englishWord.txt") as file:
        sourceword = file.read().replace("\n"," ")
        return sourceword.split(" ")