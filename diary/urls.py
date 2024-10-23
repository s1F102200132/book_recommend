# diary/urls.py
from django.urls import path
from . import views

app_name = 'diary'

urlpatterns = [
    path('new/', views.create_diary_entry, name='create_entry'),
    path('<int:pk>/', views.diary_entry_detail, name='entry_detail'),
    path('', views.diary_list, name='diary_list'),  # diary/ へのパス
]
