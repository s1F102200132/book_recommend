# diary/views.py
from django.shortcuts import render, redirect
from .models import DiaryEntry
from .utils.sentiment_analysis import analyze_sentiment

from .utils import analyze_sentiment, recommend_book_by_sentiment

from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import DiaryEntry

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
    try:
        diary_entry = DiaryEntry.objects.get(pk=pk)
    except DiaryEntry.DoesNotExist:
        raise Http404("指定された日記エントリは存在しません。")

    return render(request, 'diary/entry_detail.html', {'diary_entry': diary_entry})

def diary_list(request):
    entries = DiaryEntry.objects.all()  # すべての日記を取得
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



