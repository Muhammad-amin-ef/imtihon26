from django.contrib import admin
from .models import Tag, Article

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content')  # ⚡ typo fixed: you wrote 'context', but should be 'content'
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
