# diary/models.py
from django.db import models
from django.contrib.auth.models import User

class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    sentiment = models.CharField(max_length=50)
    recommended_book = models.CharField(max_length=100, default="Not Available")

    created_at = models.DateTimeField(auto_now_add=True)  # 追加部分

    def __str__(self):
        return self.content[:20]
    
from django.db import models

class Entry(models.Model):
    content = models.TextField()  # 例としてcontentフィールドがある場合
    # 他の必要なフィールドをここに追加

    def __str__(self):
        return self.content[:50]  # エントリの一部を返す

