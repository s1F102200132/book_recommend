from django.shortcuts import render, redirect
from .models import DiaryEntry
from .utils import analyze_sentiment, recommend_book_by_sentiment
from collections import Counter
import matplotlib.pyplot as plt
import io
import base64

def index(request):
    return render(request, 'diary/index.html')

def create_diary_entry(request):
    if request.method == "POST":
        content = request.POST.get("content")
        sentiment, confidence = analyze_sentiment(content)  # 日記の感情分析

        # 感情分析に基づいて推薦された本を取得
        recommended_book = recommend_book_by_sentiment(sentiment)

        # 日記エントリーを保存
        diary_entry = DiaryEntry.objects.create(
            user=request.user if request.user.is_authenticated else None,
            content=content,
            sentiment=sentiment,
            recommended_book=recommended_book
        )
        return redirect('diary:diary_list')
    
    return render(request, 'diary/create_entry.html')


def sentiment_dashboard(request):
    # ユーザーの日記エントリを取得
    entries = DiaryEntry.objects.filter(user=request.user)

    # 感情ごとの集計
    sentiments = []
    for entry in entries:
        sentiment, confidence = analyze_sentiment(entry.content)  # analyze_sentimentを呼び出す
        entry.sentiment = sentiment  # 感情を動的に設定
        entry.confidence = confidence  # 信頼度を設定
        sentiments.append(sentiment)

    sentiment_counts = Counter(sentiments)

    # 統計情報
    total_entries = len(entries)
    positive_count = sentiment_counts.get('positive', 0)
    negative_count = sentiment_counts.get('negative', 0)
    neutral_count = sentiment_counts.get('neutral', 0)

    # グラフ作成（Matplotlibを使用）
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie([positive_count, negative_count, neutral_count], 
           labels=['Positive', 'Negative', 'Neutral'], 
           autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#F44336', '#FFC107'])
    ax.axis('equal')  # 円形に表示

    # グラフを画像として保存
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    graph_url = base64.b64encode(img_buffer.read()).decode('utf-8')

    # ダッシュボードの統計情報とグラフをテンプレートに渡す
    context = {
        'total_entries': total_entries,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'neutral_count': neutral_count,
        'graph_url': graph_url,
        'entries': entries,
    }

    return render(request, 'diary/sentiment_dashboard.html', context)


def diary_entry_detail(request, pk):
    # 日記エントリーを取得
    diary_entry = DiaryEntry.objects.get(pk=pk)

    # 日記の感情分析
    diary_sentiment, confidence = analyze_sentiment(diary_entry.content)

    # 日記の感情に基づいて推薦された本を取得
    recommended_books = recommend_book_by_sentiment(diary_sentiment)

    # 手動で設定したレビューリスト
    book_reviews = {
        "The Happiness Project": [
            "This book is full of practical advice and uplifting insights about how to live a happier life.",
            "It's an inspiring read that really makes you think about your own life and happiness."
        ],
        "When Breath Becomes Air": [
            "A deeply emotional and profound book, truly life-changing.",
            "The author reflects on mortality and the meaning of life in a very touching way."
        ],
        "Anger: Wisdom for Cooling the Flames": [
            "A very insightful book on understanding and managing anger.",
            "It offers practical tools for controlling anger in difficult situations."
        ]
    }

    # レビューの感情分析を行い、結果を集める
    review_sentiment_results = []
    for book, reviews in book_reviews.items():
        for review in reviews:
            review_sentiment, review_confidence = analyze_sentiment(review)
            review_sentiment_results.append({
                "book_title": book,
                "review": review,
                "sentiment": review_sentiment,
                "confidence": review_confidence
            })

    # テンプレートに渡すコンテキスト
    context = {
        'diary_entry': diary_entry,
        'diary_sentiment': diary_sentiment,
        'recommended_books': recommended_books,
        'review_sentiment_results': review_sentiment_results,
    }

    return render(request, 'diary/entry_detail.html', context)


def diary_list(request):
    entries = DiaryEntry.objects.all()  # すべての日記を取得
    return render(request, 'diary/diary_list.html', {'entries': entries})
