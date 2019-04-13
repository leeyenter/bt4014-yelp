import pandas as pd
import gensim
import json
import spacy

from gensim.models import Word2Vec
from gensim.models.phrases import Phraser, Phrases

from tqdm import tqdm
tqdm().pandas()

#print("Loading spacy model")
#
#nlp = spacy.load("en_core_web_sm", disable=["parser", "ner", "textcat"])
#
#print("Loading data")
#
#review = pd.read_json('/hpctmp/e0003561/data/review.json', lines=True, orient='columns')
#business = pd.read_json("/hpctmp/e0003561/data/business.json", lines=True, orient='columns')
#cats = set()
#for category in business.categories.unique():
#    if category is not None:
#        cats.update(category.split(", "))
#foodCategories = {'food','restaurant'}
#def check_food(x):
#    if x is None:
#        return False
#    return any(foodItem in x.lower() for foodItem in foodCategories)
#business['food'] = business.categories.progress_apply(check_food)
#business = business[business.food]
#business.set_index('business_id', inplace=True)
#review = review.join(business[['food']], on='business_id', how='inner')
#review = review[review.food]
#
#skip = {'$', 'CD'}
#def tokenise(text):
#    if type(text) != str:
#        return []
#    text = text.replace('\n\n', '.').replace('\n', '.').replace('!', '.').replace('?', '.').replace('.', '. ')
#    while '  ' in text:
#        text = text.replace('  ', ' ')
#    doc = nlp(text, disable=["parser", "ner", "textcat"])
#    tokens = []
#    for token in doc:
#        if (not token.is_punct and token.tag_ not in skip):
#            if token.lemma_ == '-PRON-':
#                tokens.append(token.text.lower())
#            else:
#                tokens.append(token.lemma_)
#    return tokens
#
#tokens = list(review.text.progress_apply(tokenise))
#
#print("Done. Saving file to token.json")
#
#with open("/hpctmp/e0003561/token.json", "w") as f:
#    json.dump(tokens, f)

with open("processed_data/token.json") as f:
    tokens = json.load(f)

model = Word2Vec(
    tokens,
    size=120,
    window=10,
    min_count=10,
    workers=20)
model.train(tokens, total_examples=len(tokens), epochs=20)
model.save('model/w2v.obj')