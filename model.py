import json

import nltk
from nltk import PorterStemmer

def search_text(text, target):
    before = ["", "", ""]
    after = ["", "", ""]
    text_tokens = nltk.word_tokenize(text)
    target_tokens = nltk.word_tokenize(target)
    stemmer = PorterStemmer()
    stem_target = [stemmer.stem(word) for word in target_tokens]
    stem_text = [stemmer.stem(word) for word in text_tokens]
    if len(target_tokens) < len(text_tokens):
        for i in range(len(text_tokens) - len(target_tokens) + 1):
            if stem_target == stem_text[i:i + len(target_tokens)]: # Maybe make this into a blurry match function
                # TODO: collect previous and next 3 words
                before = (text_tokens[:i])[-3:]
                after = (text_tokens[i + len(target_tokens):])[:3]

    return before, after

if __name__ == "__main__":
    with open("./email_jsons/id000.json", "r") as file:
        data = json.load(file)
        body = data.get("body", "")
        print(body)
    print(search_text(body, "Conference on Computing Technology and Information Management"))