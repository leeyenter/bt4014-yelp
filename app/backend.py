import json
import math
import os

import numpy as np
import pandas as pd
import spacy
from flask import Flask, jsonify, send_from_directory
from tqdm import tqdm
from wordcloud import WordCloud

tqdm().pandas()

def wordcloud_from_dataframe(df, wordcloud_params=None):
    try:
        df['wordcloud_score'] = df['count'] * df['score']
        mapping = dict(map(tuple, df[['phrase', 'wordcloud_score']].values))
        WordCloud(**wordcloud_params).generate_from_frequencies(mapping).to_file('frontend/build/wordcloud.jpg')
    except Exception as e:
        print("Error in generating wordcloud.")
        print(e)
        return False
    return True

print("Loading spacy")

app = Flask(__name__, static_url_path='/frontend/build')
nlp = spacy.load("en_core_web_lg")
# import gensim
# model = gensim.models.Word2Vec.load("../models/w2v.obj")
# keys = []
# for idx in range(len(model.wv.vocab)):
#     keys.append(model.wv.index2word[idx])
# nlp.vocab.vectors = spacy.vocab.Vectors(data=model.wv.syn0, keys=keys)

print("Loading info")

shakeshack = pd.read_parquet("../data/Shake Shack_reviews.parquet")[['address', 'city', 'latitude', 'longitude']].reset_index(drop=True).drop_duplicates()
innout = pd.read_parquet("../data/In-N-Out Burger_reviews.parquet")[['address', 'city', 'latitude', 'longitude']].reset_index(drop=True).drop_duplicates()
cheesecake = pd.read_parquet("../data/The Cheesecake Factory_reviews.parquet")[['address', 'city', 'latitude', 'longitude']].reset_index(drop=True).drop_duplicates()

print("Loading reviews (1/3)")
shakeshack_reviews = pd.read_pickle("../data/phrases_Shake Shack_spacy.pkl")
print("Loading reviews (2/3)")
innout_reviews = pd.read_pickle("../data/phrases_In-N-Out Burger_spacy.pkl")
print("Loading reviews (3/3)")
cheesecake_reviews = pd.read_pickle("../data/phrases_The Cheesecake Factory_spacy.pkl")

def build_histogram(data_dict):
    output = {}
    for key, val in data_dict.items():
        hist = np.histogram(val, range=(-1, 1))
        newVal = {
            'values': [int(x) for x in hist[0]],
            'labels': [float(x) for x in hist[1]][:-1]
        }
        output[key] = newVal
    return output

@app.route("/backend/business/<biz_name>/<search_query>")
def searchQuery(biz_name, search_query):
    print(search_query, biz_name)
    search_doc = nlp(search_query)

    def calc_similarity(review_doc):
        return review_doc.similarity(search_doc)

    if biz_name == "shake-shack":
        info_df = shakeshack
        reviews = shakeshack_reviews
    elif biz_name == "in-n-out":
        info_df = innout
        reviews = innout_reviews
    else:
        info_df = cheesecake
        reviews = cheesecake_reviews

    print("Calculating review similarity")
    reviews['text_similarity'] = reviews.spacy.progress_apply(calc_similarity)
    sub_reviews = reviews.sort_values('text_similarity', ascending=False).head(500)#[reviews.text_similarity > 0.2]
    sub_phrases = sub_reviews.phrases.apply(lambda x: pd.Series(x)).unstack()
    sub_reviews = sub_reviews.drop('phrases', axis = 1).join(pd.DataFrame(sub_phrases.reset_index(level=0, drop=True))).dropna(axis=0)
    print("Calculating phrase similarity")
    sub_reviews['similarity'] = sub_reviews[0].progress_apply(calc_similarity)
    sub_reviews['similarity_score'] = sub_reviews['similarity'] + 1.3 * sub_reviews['text_similarity']

    sub_reviews = sub_reviews[sub_reviews.similarity_score >= 1.2].sort_values('similarity_score', ascending=False).drop_duplicates().head(2000)

    print("Summarising phrases (1/2)")
    phrases_found = []
    for row_index in tqdm(range(sub_reviews.shape[0])):
        row = sub_reviews.iloc[row_index]
        phrase = row[0]
        similarity_score = row['similarity_score']
        sentiment = row['sentiment']
        location = row['address'] + ', ' + row['city']
        
        found_before = False
        for phrase_set in phrases_found:
            for prev_phrase in phrase_set[0]:
                if phrase.similarity(prev_phrase) > 0.88:
                    found_before = True
                    phrase_set[0].append(phrase)
                    phrase_set[1].append(similarity_score)
                    phrase_set[2].append(sentiment)
                    phrase_set[3].append(location)
                    break
            if found_before:
                break
        if not found_before:
            phrases_found.append([[phrase], [similarity_score], [sentiment], [location]])
    print("Summarising phrases (2/2)")
    results = {}
    nlps = {}
    for phrase_set in tqdm(phrases_found):
        phrases = phrase_set[0]
        max_similarity = 0
        phrase_similarities = {}
        phrase = ''
        x = pd.Series([x.text for x in phrase_set[0]]).value_counts().sort_values(ascending=False)
        phrases = x[x == x[0]].index
        for i in range(len(phrases)):
            phrase_similarities[i] = 0
            for j in range(len(phrases)):
                if i == j:
                    continue
                if phrases[i] in nlps:
                    phrase_i = nlps[phrases[i]]
                else:
                    phrase_i = nlp(phrases[i])
                    nlps[phrases[i]] = phrase_i
                
                if phrases[j] in nlps:
                    phrase_j = nlps[phrases[j]]
                else:
                    phrase_j = nlp(phrases[j])
                    nlps[phrases[j]] = phrase_j
                
                phrase_similarities[i] += phrase_i.similarity(phrase_j)

        for i, score in phrase_similarities.items():
            if score >= max_similarity:
                max_similarity = score
                phrase = phrases[i]
                
        score = np.mean(phrase_set[1]) * math.log(len(phrase_set[1])+1)
        count = len(phrase_set[1])
        sentiments = phrase_set[2]
        locations = phrase_set[3]
        results[len(results)] = {'phrase': phrase,
                                'score': score, 
                                'count': count, 
                                'sentiments': sentiments,
                                'locations': locations}

    results = pd.DataFrame.from_dict(results, orient='index').sort_values('score', ascending=False).reset_index(drop=True).head(1000)
    
    wordcloud_from_dataframe(results, {'background_color':'white',
                                'min_font_size':3,
                                'colormap':'inferno',
                                'font_step':1})

    results_obj = json.loads(results.to_json(orient="records"))
    print("Calc location sentiments")
    location_sentiments = {}
    for i in range(info_df.shape[0]):
        location_sentiments[info_df.iloc[i]["address"] + ", " + info_df.iloc[i]["city"]] = []
    
    for i in range(results.shape[0]):
        for j in range(results.iloc[i]['count']):
            location = results.iloc[i]['locations'][j]
            sentiment = results.iloc[i]['sentiments'][j]
            if location not in location_sentiments:
                location_sentiments[location] = []
            location_sentiments[location].append(sentiment)

    print("Prepare word cloud")

    return json.dumps({
        'num_reviews': reviews.shape[0], 
        'results': results_obj,
        'location_sentiments': build_histogram(location_sentiments), 
        'reviews': json.loads(sub_reviews[['address', 'text', 'stars']].to_json(orient='records')), 
        'info': json.loads(info_df.to_json(orient='records'))
    })


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    print(path)
    if path != "" and os.path.exists("frontend/build/" + path):
        return send_from_directory('frontend/build', path)
    else:
        return send_from_directory('frontend/build', 'index.html')

@app.after_request
def add_header(r):
    """
    Add headers to force the browser to not cache static files. 
    To make it easier for development, can be safely removed 
    in production. 
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == "__main__":
    app.run(debug=False, threaded=True)