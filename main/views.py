from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .models import Article, Tag
from django.views import View


# Register View
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


# Login View
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


# Logout View
def Logout_view(request):
    logout(request)
    return redirect('/login/')


# /articles/ - BlogView: Maqolalar ro'yxatini va yangi maqola qo'shishni ko'rsatadi
class BlogView(View):
    def get(self, request):
        articles = Article.objects.all().order_by('-created_at')  # Maqolalarni chiqarish
        return render(request, 'articles.html', {'articles': articles})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/login/')  # Agar foydalanuvchi tizimga kirgan bo'lmasa, login sahifasiga yuboriladi

        title = request.POST.get('title')  # Maqola sarlavhasi
        context = request.POST.get('context')  # Maqola matni
        tag_names = request.POST.get('tags', '').split(',')  # Teglar

        slug = slugify(title)  # Slug avtomatik tarzda generatsiya qilinadi

        # Yangi maqolani yaratish
        article = Article.objects.create(
            title=title,
            context=context,
            author=request.user,
            slug=slug
        )

        # Teglarni qo'shish
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
            article.tags.add(tag)

        return redirect('/articles/')  # Maqola muvaffaqiyatli qo'shilgandan so'ng, maqolalar ro'yxatiga qaytaradi


# /articles/<slug>/ - ArticleView: Maqolaning to'liq ma'lumotini ko'rsatadi
class ArticleView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)  # Slug bo'yicha maqolani olish
        return render(request, 'article_detail.html', {'article': article})


# /my-articles/ - MyArticlesView: Foydalanuvchining o'ziga tegishli maqolalarini ko'rsatadi
@login_required
def my_articles_view(request):
    articles = Article.objects.filter(author=request.user)  # Faqat o'z maqolalari
    return render(request, 'my_articles.html', {'articles': articles})


from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
