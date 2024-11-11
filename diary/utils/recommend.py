def recommend_book_by_sentiment(sentiment):
    """
    感情に基づいて本を推薦する関数。

    Parameters:
    sentiment (str): 感情ラベル（ポジティブ、ネガティブ、ニュートラル）

    Returns:
    str: 推薦する本のタイトル
    """
    recommendations = {
        "ポジティブ": "ポジティブな気分の時に読むべき本のタイトル",
        "ネガティブ": "ネガティブな気分の時に読むべき本のタイトル",
        "ニュートラル": "ニュートラルな気分の時に読むべき本のタイトル"
    }
    return recommendations.get(sentiment, "おすすめの本はありません。")
