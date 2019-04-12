from wordcloud import Wordcloud

def wordcloud_from_dataframe(df, wordcloud_params=None):
    try:
        df['wordcloud_score'] = df['count'] * df['score']
        mapping = dict(map(tuple, temp[['phrase', 'wordcloud_score']].values))
        WordCloud(**wordcloud_params).generate_from_frequencies(mapping).to_file('wordcloud.jpg')
    except:
        print("Error in generating wordcloud.")
        return False
    return True