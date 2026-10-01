from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('ask/', views.answer_view, name='answer'),
    path('articles/', views.article_list_view, name='article_list'),
    path('articles/<int:pk>/', views.article_detail_view, name='article_detail'),
]
