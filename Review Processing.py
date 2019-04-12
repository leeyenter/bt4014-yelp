import re

import pandas as pd
import spacy
from spacy_cld import LanguageDetector
from tqdm import tqdm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

tqdm().pandas()
nlp = spacy.load("en_core_web_lg")
analyser = SentimentIntensityAnalyzer()
language_detector = LanguageDetector()
nlp.add_pipe(language_detector)

accepted_pos = {'NOUN', 'PROPN', 'ADV', 'ADJ', 'VERB', 'PRON'}
contain_pos = {'DET', 'PART', 'ADP', 'NUM'}
after_cconj_pos = {'ADV', 'ADJ', 'VERB'}
# Previously used to filter out 'allowed phrases', but in the end not used.
permitted_start_ends = {('NOUN', 'ADJ'), ('NOUN', 'VERB'), ('PROPN', 'ADJ'), 
                        ('PROPN', 'VERB'), ('ADJ', 'NOUN'), ('ADJ', 'PROPN'), 
                        ('ADV', 'VERB'), ('PROPN', 'NOUN'), ('NOUN', 'PROPN'), 
                        ('NOUN', 'NOUN'), ('PROPN', 'PROPN')}

def pull_phrases(doc):
    phrases = []
    start_index = 0 # should be inclusive
    end_index = 0 # should be exclusive

    while start_index < len(doc):
        while start_index < len(doc) and doc[start_index].pos_ not in accepted_pos:
            start_index+=1
        end_index = start_index
        while end_index < len(doc) and doc[end_index].pos_ in accepted_pos.union(contain_pos):
            end_index += 1
            if end_index < len(doc) - 1 and doc[end_index].pos_ == 'CCONJ' and doc[end_index+1].pos_ in after_cconj_pos:
                end_index += 2 # include related terms after conjunctions
        while doc[end_index-1].pos_ in contain_pos:
            end_index -= 1

        # add phrase
        if start_index >= len(doc):
            break
        if True:#(doc[start_index].pos_, doc[end_index-1].pos_) in permitted_start_ends:
            phrase = []
            for token_index in range(start_index, end_index):
                token_text = doc[token_index].lemma_
                if token_text == '-PRON-':
                    token_text = doc[token_index].text.lower()
                phrase.append(token_text)
            phrase = ' '.join(phrase)
            if len(phrase) > 1:
                phrases.append(nlp(phrase))

        # Move start_index to end_index, to continue scanning
        start_index = end_index
    return phrases

for business_name in ['Shake Shack', 'In-N-Out Burger', 'The Cheesecake Factory']:
    print(business_name)
    reviews = pd.read_pickle('data/'+business_name+'_spacy')
    print("    Applying sentiment analysis")
    reviews['sentiment'] = reviews.text.progress_apply(lambda x: analyser.polarity_scores(x)['compound'])
    print("    Filtering non-english reviews")
    reviews['is_en'] = reviews.spacy.progress_apply(lambda doc: len(doc._.languages) == 0 or doc._.languages[0] == 'en')
    reviews = reviews[reviews.is_en]
    reviews.drop('is_en', axis=1, inplace=True)
    print("    Pulling phrases")
    reviews['phrases'] = reviews.spacy.progress_apply(pull_phrases)
    reviews = reviews[reviews.phrases.apply(lambda x: len(x) > 0)]
    print("    Saving file")
    reviews.to_pickle("data/phrases_" + business_name + "_spacy.pkl")