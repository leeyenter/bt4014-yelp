from flask import Flask, send_from_directory, jsonify
import pandas as pd
import numpy as np
import json

app = Flask(__name__)

shakeshack = pd.read_parquet("../data/Shake Shack_reviews.parquet")[['address', 'city', 'latitude', 'longitude']].reset_index(drop=True).drop_duplicates()

@app.route("/backend/business/<biz_name>/<search_query>")
def searchQuery(biz_name, search_query):
    results = pd.read_json("../processed_data/tmp_search_results.json")
    return results.to_json(orient="records")

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


@app.route("/backend/business/<biz_name>/")
def searchQueryEmpty(biz_name):
    results = pd.read_json("../processed_data/tmp_search_results.json")
    results_obj = json.loads(results.to_json(orient="records"))
    
    location_sentiments = {}
    for i in range(results.shape[0]):
        for j in range(results.iloc[i]['count']):
            location = results.iloc[i]['locations'][j]
            sentiment = results.iloc[i]['sentiments'][j]
            if location not in location_sentiments:
                location_sentiments[location] = []
            location_sentiments[location].append(sentiment)
    

    return jsonify({
        'results': results_obj,
        'location_sentiments': build_histogram(location_sentiments), 
        'info': json.loads(shakeshack.to_json(orient='records'))
    })

@app.route("/")
def facultyIndex(path):
    '''Serves the faculty portal '''
    return send_from_directory('faculty', path)

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
    app.run(debug=True, threaded=True)