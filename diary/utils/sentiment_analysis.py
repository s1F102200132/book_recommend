from textblob import TextBlob

def analyze_sentiment(text):
    """
    指定されたテキストの感情分析を行う関数。

    Parameters:
    text (str): 分析するテキスト

    Returns:
    str: ポジティブ、ネガティブ、またはニュートラルの感情ラベル
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1から1の範囲で感情の極性を取得

    if polarity > 0:
        return "ポジティブ"
    elif polarity < 0:
        return "ネガティブ"
    else:
        return "ニュートラル"
