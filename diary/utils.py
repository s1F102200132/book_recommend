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


