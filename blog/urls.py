from django.contrib import admin
from django.urls import path,include
from .views import Index,DetailArticleView,LikeArticle,Featured,DeleteArticleView,create_article,UpdateArticleView
from . import views
urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('', Index.as_view(), name = 'index'),
    path('<int:pk>/',DetailArticleView.as_view(), name='detail_article'),
    path('<int:pk>/like',LikeArticle.as_view(),name='like_article'),
    path('featured/',Featured.as_view(),name='featured'),
    path('<int:pk>/delete', DeleteArticleView.as_view(),name='delete_article'),
    path('create/', views.create_article, name='create_article'),
    path('<int:pk>/edit/', UpdateArticleView.as_view(), name='edit_article'),

    
]