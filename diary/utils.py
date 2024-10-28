# diary/utils.py
from textblob import TextBlob

def analyze_sentiment(content):
    analysis = TextBlob(content)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity == 0:
        return "Neutral"
    else:
        return "Negative"
    

