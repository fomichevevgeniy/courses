from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Тут прописываются модели, на основе которых
# Создадутся таблицы базы данных и их
# Вид и дополнительные функции для работы с ними

# Create your models here.
class Category(models.Model):
    # id создавать не обязательно . Django сделает его сам
    title = models.CharField(max_length=255, verbose_name='Название категории')
    # title VARCHAR(255)
    theme = models.CharField(max_length=255, verbose_name='Цветовая схема')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название статьи')
    content = models.TextField(default='Здесь будет текст', verbose_name='Описание')
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='Изображение')
    # blank = True - можно не заполнять это поле, null = True - может быть пустым в базе
    youtube_link = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ссылка на видео')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    # Научит модель переходить на саму себя
    def get_absolute_url(self):
        return reverse('article', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


# Создать модель Comment
# Которая знает Статью Пользователя Текст и Дату
# Создать форму для заполнения текста
# Улучшить Детали Статьи чтобы выводить форму, только если зарегестрировать
# Прописать вьюшку для сохранения комментария
# Доработать детали статьи для вывода комментариев
# Сделать куски HTML для вывода формы и комментариев


class Comment(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
