# diary/views.py
from django.shortcuts import render, redirect
from .models import DiaryEntry
from .utils import analyze_sentiment, recommend_book_by_sentiment

#def home(request):
    #return render(request, 'home.html')

def create_diary_entry(request):
    if request.method == "POST":
        content = request.POST.get("content")
        sentiment = analyze_sentiment(content)
        recommended_book = recommend_book_by_sentiment(sentiment)
        
        diary_entry = DiaryEntry.objects.create(
            user=request.user,
            content=content,
            sentiment=sentiment,
            recommended_book=recommended_book
        )
        return redirect('diary:entry_detail', pk=diary_entry.pk)
    
    return render(request, 'diary/create_entry.html')

def diary_entry_detail(request, pk):
    diary_entry = DiaryEntry.objects.get(pk=pk)
    return render(request, 'diary/entry_detail.html', {'diary_entry': diary_entry})

def diary_list(request):
    entries = DiaryEntry.objects.all()  # すべての日記を取得
    return render(request, 'diary/diary_list.html', {'entries': entries})
