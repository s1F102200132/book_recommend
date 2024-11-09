# diary/views.py
from django.shortcuts import render, redirect
from .models import DiaryEntry
from .utils import analyze_sentiment, recommend_book_by_sentiment, get_amazon_reviews

#def home(request):
    #return render(request, 'home.html')

def index(request):
    return render(request, 'diary/index.html')
    

def create_diary_entry(request):
    if request.method == "POST":
        content = request.POST.get("content")
        sentiment = analyze_sentiment(content)
        recommended_book = recommend_book_by_sentiment(sentiment)

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

    # 書籍のレビューを取得し、レビューの感情分析を行う
    review_sentiment_results = []
    for book in recommended_books:
        reviews = get_amazon_reviews(book)
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
