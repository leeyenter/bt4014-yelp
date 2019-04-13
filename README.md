# Analysing Yelpers’ Behaviour and Reviews to Drive Business Insights

## Introduction



### Project Structure

The Yelp dataset is expected to reside in the `data` folder. 
The directory structure should thus be:

```
data
├── business.json
├── checkin.json
├── photo.json (unused, can be deleted)
├── review.json
├── tip.json (unused, can be deleted)
└── user.json
```

### Python Packages Used

* Flask>=1.0.2 (for the web app)
* Gensim>=3.5.0
* NLTK>=3.2.1
* Numpy>=1.14.2
* Pandas>=0.22.0
* progressbar2 (non-essential)
* PyArrow>=0.13.0
* Seaborn>=0.9.0
* Spacy>=2.0.11
* spacy-cld>=0.1.0
* StatsModels>=0.9.0
* tabulate (non-essential)
* tqdm>=4.28.1 (non-essential)
* VaderSentiment>=3.2.1
* Wordcloud>=1.5.0

## Description of Jupyter Notebooks & Python Scripts

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `Load Data.ipynb` | Subsets the full Yelp dataset, so that we can easily work with it to develop algorithms first. Subsequent analyses is then done on the full dataset. | Original Yelp data (e.g. `data/review.json`) | Sampled data in Parquet format (e.g. `data/<num_reviews>_review.parquet`) |
| `Load Data.py` | Generates 'proper' samples of varying sizes, instead of taking the first few reviews. Involves loading the entire dataset into memory. | Original Yelp data (e.g. `data/review.json`) | Sampled data in Parquet format (e.g. `data/<num_reviews>_review.parquet`) |
| `EDA.ipynb` | Conducts some EDA on the subsetted data | Sampled data in Parquet format (e.g. `data/<num_reviews>_review.parquet`) | _(none)_ |
| `Business EDA.ipynb` | Conducts some EDA on the businesses. | `data/review.json`, `data/business.json` | _(none)_ |
| `Tokenise.py` | Uses Spacy to tokenise the `review.json` data | `data/review.json` | `processed_data/token.json` |
| `LDA - Model Building & Evalution.ipynb` | Prepares the corpus and dictionary for all reviews, and conducts grid search to find the top few LDA models. Also displays topic distribution for the models. | `processed_data/token.json` | `processed_data/corpus.json`, `processed_data/corpus.pkl`, `processed_data/dictionary`, and various models in `models/lda` |
| `Train W2V.py` | Trains a Word2Vec model on all reviews on food-related businesses. | `data/review.json`, `data/business.json` | `processed_data/token.json`, `model/w2v.obj` |
| `Review Selection & Loading.ipynb` | Selects all reviews for a given company, and use Spacy on the review text. Saves the data as a Parquet file (for non-Spacy dataframe) and a pickle file (with Spacy) | `data/business.json`, `data/review.json` | `data/<company_name>_reviews.parquet`, `data/<company_name>_spacy` | 
| `LDA - Business Reviews.ipynb` | Given a company name, build the corpus and dictionary specific for that company's reviews, and conduct a grid search on LDA models for that company. Also displays modal topics. | `data/<company_name>_reviews.parquet` | _(none)_ |
| `Review Processing.py` | Processes company reviews from the above notebook, by applying sentiment analysis and splitting the review texts into phrases using POS tagging. Also applies Spacy onto the review text and phrases, to reduce the processing time in the future. | `data/<company_name>_spacy` | `data/<company_name>_spacy.pkl` | 
| `Search Phrases from Reviews.ipynb` | Given a company name and a search query, select relevant phrases from reviews about that company's various branches. | `data/<company_name>_spacy.pkl` | _(none)_ |
| `IRF.ipynb` | Performs Impulse Response analysis on the 3 companies. | `data/review.json`, `data/business.json`, `data/user.json`, `data/checkin.json` | _(none)_ |
| `Wordcloud.py` | Creates wordcloud from the processed review data, for reports and web app | `processed_data/tmp_search_results.json` | _wordcloud.jpg_ |

## Web App

In order to run the web app, there are 2 steps:

1. Run the backend (will take a while to load):

    ```shell
    cd app
    python backend.py
    ```

2. Run the frontend (requires `npm` to be installed):

    ```shell
    cd app/frontend
    npm i
    npm start
    ```

3. A browser window should open, pointing you to http://localhost:3000. 

If the page keeps refreshing when the search has completed, you may want to build the React frontend first, then load it using Flask:

```shell
cd app/frontend
npm run build
```

Then, visit http://localhost:5000 instead of the above link. 

Do note that you will need to have the `data/<company_name>_reviews.parquet` and `data/phrases_<company_name>_spacy.pkl` files loaded for all the companies that you want to analyse. 