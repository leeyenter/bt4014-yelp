print("Importing libraries")
import pandas as pd
import gensim
import json, pickle
import spacy

from tqdm import tqdm
tqdm().pandas()

print("Loading spacy model")

nlp = spacy.load("en_core_web_sm", disable=["parser", "ner", "textcat"])

print("Loading data")

review = pd.read_json('data/review.json', lines=True, orient='columns')
review.set_index('review_id', inplace=True)

skip = {'$', 'CD', "POS"}
def tokenise(text):
    if type(text) != str:
        return []
    text = text.replace('\n\n', '.').replace('\n', '.').replace('.', '. ')
    while '  ' in text:
        text = text.replace('  ', ' ')
    doc = nlp(text, disable=["parser", "ner", "textcat"])
    tokens = [token.lemma_ for token in doc if (not token.is_stop and not token.is_punct and token.tag_ not in skip and len(token) > 2)]
    return tokens

tokens = list(review.text.progress_apply(tokenise))

print("Done. Saving file to token.json")

with open("processed_data/token.json", "w") as f:
    json.dump(tokens, f)