import nltk
from nltk.corpus import stopwords
import ssl
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

from utils import logger

# Credit for https://stackoverflow.com/questions/38916452/nltk-download-ssl-certificate-verify-failed to avoid CERTIFICATE_VERIFY_FAILED error in nltk
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download("stopwords", quiet=True)
nltk.download("vader_lexicon", quiet=True)

# Returns a panda dataframe from all comments
def create_dataframe(comments):
    df = pd.DataFrame(list(comments), columns=["Raw Comments"])
    return df

# Clean the comments (e.g. remove stop words) from dataframe for sentiment analysis, returns the cleaned df
def clean_comments(dataframe):
    dataframe["Cleaned Comments"] = (
        dataframe["Raw Comments"]
        .str.strip()
        .str.replace("\n", " ")
        .str.lower()
        # remove numbers
        .str.replace(r"\d+", "", regex=True)
        # remove hashtags
        .str.replace(r"#\S+", " ", regex=True)
        # Credit for https://stackoverflow.com/questions/13896056/how-to-remove-user-mentions-and-urls-in-a-tweet-string-using-python
        # remove mentions and links
        .str.replace(r"(?:\@|https?\://|www)\S+", "", regex=True)
        # remove special chars and emojis
        .str.replace(r"[^\w\s]+", "", regex=True)
    )

    dataframe["Cleaned Comments"] = dataframe["Cleaned Comments"].apply(
        lambda comment: " ".join([word for word in comment.split() if word not in stopwords.words("english")])
    )

    return dataframe

# Analyze comments by computing polarity score and classify to sentiments
def analyze_comments(dataframe):
    dataframe["Sentiment Score"] = dataframe["Cleaned Comments"].apply(
        lambda comment: _calculate_polarity_score(SentimentIntensityAnalyzer(), comment)
    )

    dataframe["Sentiment"] = dataframe["Sentiment Score"].apply(
        lambda score: _get_sentiment(score)
    )

    return dataframe


def _calculate_polarity_score(analyzer, text):
    scores = analyzer.polarity_scores(text)
    return scores["compound"]


def _get_sentiment(score):
    sentiment = ""
    if score <= -0.5:
        sentiment = "Negative"
    elif -0.5 < score <= 0.5:
        sentiment = "Neutral"
    else:
        sentiment = "Positive"

    return sentiment
