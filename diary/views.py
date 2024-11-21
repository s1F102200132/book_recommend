from django.shortcuts import render, redirect, get_object_or_404
from .models import DiaryEntry
from .utils import analyze_sentiment, recommend_book_by_sentiment
import calendar
from datetime import datetime  # これを追加


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
    # 現在の日付を取得
    today = datetime.today()
    current_year = today.year
    current_month = today.month
    current_day = today.day

    # 表示する月を取得（クエリパラメータがあればそれを使い、なければ現在の月）
    year = int(request.GET.get('year', current_year))
    month = int(request.GET.get('month', current_month))

    # 前月、次月を計算
    prev_year, prev_month = (year, month - 1) if month > 1 else (year - 1, 12)
    next_year, next_month = (year, month + 1) if month < 12 else (year + 1, 1)

    # 月の日数と最初の日が何曜日かを取得
    month_days = calendar.monthrange(year, month)[1]
    first_weekday = calendar.monthrange(year, month)[0]  # 0:月曜日、6:日曜日

    # 曜日をリストで定義
    weekdays = ["月", "火", "水", "木", "金", "土", "日"]

    # カレンダーの空のグリッドを作成（最大6行）
    calendar_grid = [[] for _ in range(6)]  

    # 最初の日曜日まで空のセルを埋める
    current_day_of_month = 1
    for row in calendar_grid:
        while len(row) < 7:
            if current_day_of_month == 1:  # 最初の週
                for _ in range(first_weekday):
                    row.append(None)  # 空のセル
                row.append(current_day_of_month)  # 最初の日
                current_day_of_month += 1
            elif current_day_of_month <= month_days:
                row.append(current_day_of_month)
                current_day_of_month += 1
            else:
                row.append(None)  # 空のセル
        if current_day_of_month > month_days:
            break

    # 本日の日付がある場合、そのセルに特別なクラスを付ける
    highlighted_day = today.day if year == current_year and month == current_month else None

    return render(request, 'diary/calendar.html', {
        'year': year,
        'month': month,
        'weekdays': weekdays,
        'calendar_grid': calendar_grid,  # カレンダーグリッド
        'today': today,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'highlighted_day': highlighted_day,  # 本日の日付を強調
    })