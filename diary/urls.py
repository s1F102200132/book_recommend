# diary/urls.py
from django.urls import path
from . import views

app_name = 'diary'

urlpatterns = [
    path('new/', views.create_diary_entry, name='create_entry'),
<<<<<<< HEAD
    path('entry/<int:pk>/', views.entry_detail, name='entry_detail'),
    path('', views.index, name='index'),
    path('diary/',views.diary_list, name='diary_list')# diary/ へのパス
=======
    path('<int:pk>/', views.diary_entry_detail, name='entry_detail'),
    path('', views.index, name='top_page'),
    path('diary/', views.diary_list, name='diary_list'),# diary/ へのパス
>>>>>>> sentiment_analysis
]
