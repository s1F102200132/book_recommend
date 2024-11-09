# diary/utils.py
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from googletrans import Translator
from deep_translator import GoogleTranslator

# モデルとトークナイザーの設定
model_name = "monologg/bert-base-cased-goemotions-original"  # 感情分析モデル
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# GoEmotionsのラベルリスト
goemotions_labels = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring", 
    "confusion", "curiosity", "desire", "disappointment", "disapproval", 
    "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief", 
    "joy", "love", "nervousness", "optimism", "pride", "realization", 
    "relief", "remorse", "sadness", "surprise", "neutral"
]

# 翻訳用の初期化
translator = Translator()

def analyze_sentiment(text):
    try:
        # テキストを翻訳
        translated_text = GoogleTranslator(source='ja', target='en').translate(text)
        print(f"翻訳文: {translated_text}")
    except Exception as e:
        print(f"翻訳中にエラーが発生しました: {e}")
        return None, 0  # エラーの場合はNoneと0を返す

    # テキストのトークナイズ
    inputs = tokenizer(translated_text, return_tensors="pt")
    
    # モデルを推論モードに設定
    with torch.no_grad():
        logits = model(**inputs).logits

    # ソフトマックス関数を使って確信度を計算
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    sentiment = torch.argmax(probabilities).item()
    confidence = probabilities[0][sentiment].item()

    # 感情ラベルの取得
    label = goemotions_labels[sentiment]

    return label, confidence


# diary/utils.py
import requests
from bs4 import BeautifulSoup

def get_amazon_reviews(book_title):
    search_url = f"https://www.amazon.com/s?k={book_title.replace(' ', '+')}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    reviews = []
    for review in soup.select('.review-text-content span'):
        reviews.append(review.get_text())
    
    return reviews

def recommend_book_by_sentiment(sentiment):
    # シンプルな例: 感情に応じた書籍タイトルを指定（後で改善）
    if sentiment == "joy":
        return "The Happiness Project"
    elif sentiment == "sadness":
        return "When Breath Becomes Air"
    elif sentiment == "anger":
        return "Anger: Wisdom for Cooling the Flames"
    elif sentiment == "fear":
        return "Feel the Fear and Do It Anyway"
    elif sentiment == "love":
        return "The 5 Love Languages"
    elif sentiment == "disgust":
        return "The Gift of Fear"
    elif sentiment == "surprise":
        return "Surprised by Joy"
    elif sentiment == "anticipation":
        return "The Power of Now"
    else:
        return "The Subtle Art of Not Giving a F*ck"