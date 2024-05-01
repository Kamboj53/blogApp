from django.contrib import admin
from django.urls import path
from . import views

app_name = "blogs"

urlpatterns = [
    path('index',views.index, name = "index"),
    path('register/',views.register,name = "register"),
    path('login/',views.loginUser,name = "login"),
    path('logout/',views.logoutUser,name = "logout"),
    path("article_detail/<int:pk>", views.ArticleDetailView.as_view(), name="article_detail"),
    path("articles", views.ArticleListView.as_view(), name="article_list"),
    path("comment/<int:pk>", views.comments, name="comment"),
]