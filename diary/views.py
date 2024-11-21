from django.shortcuts import render, redirect, get_object_or_404
from .models import DiaryEntry
from .utils import analyze_sentiment, recommend_book_by_sentiment

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
    # 新しい日記エントリーを上に表示するように変更
    entries = DiaryEntry.objects.all().order_by('-created_at')  # created_atフィールドで降順にソート
    return render(request, 'diary/diary_list.html', {'entries': entries})


def delete_diary_entry(request, pk):
    diary_entry = get_object_or_404(DiaryEntry, pk=pk)
    if request.method == "POST":
        diary_entry.delete()
        return redirect('diary:diary_list')
    return render(request, 'diary/confirm_delete.html', {'diary_entry': diary_entry})

def calendar_view(request):
    return render(request, 'diary/calendar.html')  # 修正: diary に変更