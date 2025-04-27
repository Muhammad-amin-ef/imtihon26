from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.Logout_view, name='logout'),
    path('articles/', views.BlogView.as_view(), name='articles'),
    path('articles/<slug:slug>/', views.ArticleView.as_view(), name='article_detail'),
    path('my-articles/', views.my_articles_view, name='my_articles'),
]



