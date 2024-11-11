from django.shortcuts import render, redirect
from .models import DiaryEntry
from .utils.sentiment_analysis import analyze_sentiment

from .utils import analyze_sentiment, recommend_book_by_sentiment

<<<<<<< HEAD
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import DiaryEntry

#def home(request):
    #return render(request, 'home.html')

=======
>>>>>>> sentiment_analysis
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

<<<<<<< HEAD


def diary_entry_detail(request, pk):
    try:
        diary_entry = DiaryEntry.objects.get(pk=pk)
    except DiaryEntry.DoesNotExist:
        raise Http404("指定された日記エントリは存在しません。")

    return render(request, 'diary/entry_detail.html', {'diary_entry': diary_entry})
=======
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
>>>>>>> sentiment_analysis

def diary_list(request):
    # 新しい日記エントリーを上に表示するように変更
    entries = DiaryEntry.objects.all().order_by('-created_at')  # created_atフィールドで降順にソート
    return render(request, 'diary/diary_list.html', {'entries': entries})



# amz_review_scraper.py
from django.shortcuts import render, get_object_or_404
from .models import Entry
from .utils.scraper import get_asin_from_amazon, get_page_from_amazon
from .utils.sentiment_analysis import analyze_sentiment

def entry_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    
    # ここでは、日記エントリにAmazonのURLがあると仮定しています
    amazon_url = entry.amazon_url  # 実際のフィールド名に変更してください
    
    asin = get_asin_from_amazon(amazon_url)
    page_content = get_page_from_amazon(amazon_url)
    
    context = {
        'entry': entry,
        'asin': asin,
        'page_content': page_content,
    }
    
    return render(request, 'your_app/entry_detail.html', context)


def get_asin_from_amazon(url):
    """
    Amazonの商品URLからASINを取得する関数。
    
    Parameters:
    url (str): Amazonの商品ページのURL
    
    Returns:
    str: 商品のASIN
    """
    from urllib.parse import urlparse, parse_qs

    parsed_url = urlparse(url)
    if 'amazon.co.jp' in parsed_url.netloc:
        asin = parse_qs(parsed_url.query).get('asin')
        return asin[0] if asin else None
    return None

def get_page_from_amazon(url):
    """
    Amazonの商品ページのコンテンツを取得する関数。
    
    Parameters:
    url (str): Amazonの商品ページのURL
    
    Returns:
    str: 商品ページのHTMLコンテンツ
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text  # HTMLコンテンツを返す
    else:
        return None  # エラー時にはNoneを返す



