from django.contrib import admin
from .models import Category, Article
# Register your models here.
from django.utils.html import format_html
# Тут прописывается логика отображения админ панели сайта
# Что будет видеть админ
# Дополнительные окна, кнопки и их дизайн

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'color_theme']
    list_display_links = ['id', 'title']

    def color_theme(self, obj):
        return format_html(f'''<div style="width: 15px; height: 15px; background-color: {obj.theme};"></div>''')

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'views']
    list_display_links = ['id', 'title']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)