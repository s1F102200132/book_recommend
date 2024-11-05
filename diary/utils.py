# diary/utils.py
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from googletrans import Translator
from deep_translator import GoogleTranslator

# モデルとトークナイザーの設定
model_name = "textattack/bert-base-uncased-SST-2"  # 感情分析モデル
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

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

    # 感情のラベルを設定
    if sentiment == 1:  # positive
        label = "POSITIVE"
    else:  # negative
        label = "NEGATIVE"

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
    if sentiment == "Positive":
        return "The Power of Positive Thinking"
    elif sentiment == "Negative":
        return "When Things Fall Apart"
    else:
        return "The Subtle Art of Not Giving a F*ck"
