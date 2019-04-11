from wordcloud import Wordcloud

def wordcloud_from_dataframe(df, wordcloud_params=None):
    """Generates wordcloud figure from a Pandas dataframe."""
    df['wordcloud_score'] = df['count'] * df['score']
    mapping = dict(map(tuple, temp[['phrase', 'wordcloud_score']].values))
    return WordCloud(**wordcloud_params).generate_from_frequencies(mapping)