from django.urls import path

from .views import ArticleListView, ArticleCRUDView, get_csrf_token_view

app_name = "api_v1"

urlpatterns = [
    path('get-csrf-token/', get_csrf_token_view),
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleCRUDView.as_view(), name='article-crud-view'),
]