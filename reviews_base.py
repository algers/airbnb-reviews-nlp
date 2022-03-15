# import numpy as np # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

# import matplotlib.pyplot as plt
from nltk.stem.snowball import SnowballStemmer
from wordcloud import WordCloud
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from sklearn import decomposition


stemmer = SnowballStemmer("english")

import os

reviews = pd.read_csv("./input/reviews_l12m_1.csv", header=0, encoding="latin-1")

print(reviews.shape)

import re


def clean_text(string_in):
    string_in = re.sub(
        "[^a-zA-Z]", " ", str(string_in)
    )  # Replace all non-letters with spaces
    string_in = string_in.lower()  # Tranform to lower case

    return string_in.strip()


reviews["comments_cleaned"] = reviews.concat_comments.apply(clean_text)


preprocessed = [
    " ".join(RegexpTokenizer(r"\w+").tokenize(reviews.comments_cleaned[idx]))
    for idx in reviews.index
]

custom_stop_words = [
    "airbnb",
    "zencity",
    "null",
    "did",
    "thank",
    "thanks",
    "definitely",
    "just",
    "got",
    "like",
    "good",
    "day",
    "great",
    "nice",
    "didnt",
    "did",
    "told",
    "bad",
    "didn",
    "unit",
    "units",
    "said",
    "bnb",
    "given",
    "dont",
    "don",
]

my_stop_words = text.ENGLISH_STOP_WORDS.union(custom_stop_words)

vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1, 1), stop_words=my_stop_words)

tfidf = vectorizer.fit_transform(preprocessed)
print("Created document-term matrix of size %d x %d" % (tfidf.shape[0], tfidf.shape[1]))


nmf = decomposition.NMF(init="nndsvd", n_components=5, max_iter=10000)
W = nmf.fit_transform(tfidf)
H = nmf.components_
print(
    "Generated W(document-topic)) matrix of size %s and H (topic-word) matrix of size %s"
    % (str(W.shape), str(H.shape))
)

feature_names = vectorizer.get_feature_names()
n_top_words = 2

for topic_idx, topic in enumerate(H):
    print("Topic #%d:" % topic_idx)
    print(
        " ".join([feature_names[i] for i in topic.argsort()[: -n_top_words - 1 : -1]])
    )


mydf = pd.DataFrame({"feature_name": feature_names})

for topic_idx, topic in enumerate(H):
    mydf["topic_" + str(topic_idx)] = topic

mylist = list(mydf.itertuples())

reviews_topic0 = []
reviews_topic1 = []
reviews_topic2 = []
reviews_topic3 = []
reviews_topic4 = []
reviews_topic_all = []

for order_id, key, num1, num2, num3, num4, num5 in mylist:
    reviews_topic0.append((key, num1))
    reviews_topic_all.append((key, num1))
    reviews_topic1.append((key, num2))
    reviews_topic_all.append((key, num2))
    reviews_topic2.append((key, num3))
    reviews_topic_all.append((key, num3))
    reviews_topic3.append((key, num4))
    reviews_topic_all.append((key, num4))
    reviews_topic4.append((key, num5))
    reviews_topic_all.append((key, num5))


reviews_topic0 = sorted(reviews_topic0, key=lambda myword: myword[1], reverse=True)
reviews_topic1 = sorted(reviews_topic1, key=lambda myword: myword[1], reverse=True)
reviews_topic2 = sorted(reviews_topic2, key=lambda myword: myword[1], reverse=True)
reviews_topic3 = sorted(reviews_topic3, key=lambda myword: myword[1], reverse=True)
reviews_topic4 = sorted(reviews_topic4, key=lambda myword: myword[1], reverse=True)


def draw_wordcloud(dict, topic_number):
    wc = WordCloud(max_words=1000)
    wordcloud = (
        WordCloud()
        .generate_from_frequencies(dict)
        .to_file("output/base/1/topic_" + str(topic_number) + ".png")
    )

    # plt.title('Topic %s' %str(topic_number), size = 16)
    # plt.imshow(wordcloud, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()


draw_wordcloud(dict(reviews_topic0), topic_number=0)
draw_wordcloud(dict(reviews_topic1), topic_number=1)
draw_wordcloud(dict(reviews_topic2), topic_number=2)
draw_wordcloud(dict(reviews_topic3), topic_number=3)
draw_wordcloud(dict(reviews_topic4), topic_number=4)
