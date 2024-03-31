from django.shortcuts import render, redirect
from .models import Category, Article, Comment
from .forms import ArticleForm, LoginForm, RegisterForm, CommentForm
from django.contrib.auth import logout, login
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

# Create your views here.

# Тут прописываются контроллеры приложения
# Которые берут данные из базы и отправляют на какую то страницу
# Или обрабатывают полученные данные и сохраняют их


def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'courses/index.html', context)

# Класс для отображения главной страницы
# ListView - класс для отображения списка объектов
class IndexView(ListView):
    model = Article  # Поле которое указывает из какой модели брать список объектов
    # По умолчанию класс будет брать ВСЕ объекты этой модели
    template_name = 'courses/index.html'  # article_list.html по умолчанию
    # Поле которое указывает в какой html шаблон будут отправляться данные. Где искать
    context_object_name = 'articles' # под именем objects будет по умолчанию
    # Под каким именем будет отправляться список объектов на страницу
    extra_context = {
        'title': 'Главная страница'
    }

def category_view(request, pk): # pk - Primary key - id категории

    # Как вывести 1 объект из базы
    category = Category.objects.get(pk=pk)
    # Как вывести статьи по условию
    articles = Article.objects.filter(category=category)
    context = {

        'articles': articles
    }
    return render(request, 'courses/index.html', context)


class CategoryView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'courses/index.html'

    # Переназначить вывод объектов
    def get_queryset(self):
        # В сcылке path('category/<int:pk>, CategoryView.as_view()')
        # Передается pk. Так как view написана на классе
        # То все дополнительные аргументы передаются в kwargs
        return Article.objects.filter(category_id=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'Категория: {category.title}'
        return context



# Вывести детали статьи
# Как делать формы для создания статей чтобы пользователь создавал
def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article
    }
    return render(request, 'courses/article_detail.html', context)


class ArticleDetail(DetailView):
    model = Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article = Article.objects.get(pk=self.kwargs['pk'])
        comments = Comment.objects.filter(article=article)
        context['comments'] = comments
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        context['title'] = f'Статья: {article.title}'
        return context

def save_comment(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = Article.objects.get(pk=pk)
            comment.user = request.user
            comment.save()
            return redirect('article', pk)


def create_article(request):
    # 2 режима
    # GET - открытие страницы
    # POST - отправка данных пользователей
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            return redirect('article', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form
    }
    return render(request, 'courses/article_form.html', context)


class CreateArticle(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'courses/article_form.html'
    extra_context = {
        'title': 'Создание новой статьи'
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateArticle(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'courses/article_form.html'
    extra_context = {
        'title': 'Изменение статьи'
    }

class DeleteArticle(DeleteView):
    model = Article
    context_object_name = 'article'
    success_url = reverse_lazy('index')  # Куда переходить, после удаления



# Изучаем как писать views на классах
# Сделать 6 классов
# Начать писать формы для логики и регистрации

def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return redirect('index')
            else:
                return redirect('login')
        else:
            return redirect('login')
    else:
        form = LoginForm()

    context = {
        'form': form,
        'title': 'Войти в аккаунт'
    }
    return render(request, 'courses/user_form.html', context)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        else:
            return redirect('register')
    else:
        form = RegisterForm()
    context = {
        'form': form,
        'title': 'Регистрация пользователя'
    }
    return render(request, 'courses/user_form.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')


def profile(request, pk):
    user = User.objects.get(pk=pk)
    articles = Article.objects.filter(author=user)
    context = {
        'user': user,
        'articles': articles,
        'title': 'Страница пользователя'
    }
    return render(request, 'courses/profile.html', context)
