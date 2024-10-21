from django.db import models

# Create your models here.
# diary/models.py
from django.db import models
from django.contrib.auth.models import User

class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sentiment = models.CharField(max_length=255, null=True, blank=True)
    recommended_book = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Diary by {self.user} on {self.created_at}"
