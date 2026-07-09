from django.contrib import admin
from .models import Category, Tag, Article,ContactMessage

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display        = ('title', 'author', 'category')
    list_filter         = ('status', 'category', 'created_at')
    search_fields       = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}


    def publish_articles(self, request, queryset):
        queryset.update(status='published')
    publish_articles.short_description = "Tanlanganllarni nashr et"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display        = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display        = ('name',)

admin.site.register(ContactMessage)