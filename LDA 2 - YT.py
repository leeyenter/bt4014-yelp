import json, pickle
import gensim
from gensim.models import CoherenceModel

if __name__ == "__main__":
    print("Loading dictionary")

    dictionary = gensim.corpora.Dictionary.load('processed_data/dictionary')
    dictionary.filter_extremes(no_below=20, no_above=0.5, keep_n=None)

    print("Loading corpus")

    with open("processed_data/corpus.json", "r") as f:
        corpus = json.load(f)

    for num_topics in [5, 10, 15, 20, 25, 30]:
        print("Num topics:", num_topics)
        lda_model = gensim.models.ldamulticore.LdaMulticore(corpus=corpus,
                                                            id2word=dictionary,
                                                            num_topics=num_topics, 
                                                            random_state=1,
                                                            chunksize=2000,
                                                            passes=4,
                                                            workers=7,
                                                            per_word_topics=True)
        #print("    Done, calculating coherence...")
        #cm = CoherenceModel(model=lda_model, corpus=corpus, coherence='u_mass')
        #coherence = cm.get_coherence()  # get coherence value
        #print("    Coherence:", coherence)
        lda_model.save("models/lda/4-passes_" + str(num_topics) + "-topics")