# diary/views.py
from django.shortcuts import render, redirect
from .models import DiaryEntry
from .utils import analyze_sentiment, recommend_book_by_sentiment

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
    diary_entry = DiaryEntry.objects.get(pk=pk)
    
    # 感情分析を実行
    sentiment, confidence = analyze_sentiment(diary_entry.content)
    
    # 結果をテンプレートに渡す
    emotion_scores = {sentiment: confidence}  # 感情スコアの辞書を作成

    return render(request, 'diary/entry_detail.html', {
        'diary_entry': diary_entry,
        'emotion_scores': emotion_scores,
    })


def diary_list(request):
    entries = DiaryEntry.objects.all()  # すべての日記を取得
    return render(request, 'diary/diary_list.html', {'entries': entries})
