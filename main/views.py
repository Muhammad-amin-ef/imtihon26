from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .models import Article, Tag
from django.views import View


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/articles/')
        return render(request, 'register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/articles/')
        return render(request, 'login.html', {'form': form})


def Logout_view(request):
    logout(request)
    return redirect('/login/')


class BlogView(View):
    def get(self, request):
        articles = Article.objects.all().order_by('-created_at')
        return render(request, 'articles.html', {'articles': articles})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/login/')

        title = request.POST.get('title')
        context = request.POST.get('context')
        tag_names = request.POST.get('tags', '').split(',')

        slug = slugify(title)

        article = Article.objects.create(
            title=title,
            context=context,
            author=request.user,
            slug=slug
        )

        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
            article.tags.add(tag)

        return redirect('/articles/')


class ArticleView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        return render(request, 'article_detail.html', {'article': article})


@login_required
def my_articles_view(request):
    articles = Article.objects.filter(author=request.user)
    return render(request, 'my_articles.html', {'articles': articles})


def home(request):
    return render(request, 'home.html')
