from django.urls import path
from .views import *

# локальные пути приложения, вынесенные в отдельный файл,
# чтобы не забивать главные urls
# тут прописывается список путей приложения


urlpatterns = [
    # path('', index, name='index'),
    # path('category/<int:pk>/', category_view, name='category'),
    # path('article/<int:pk>/', article_detail, name='article'),
    # path('create_article/', create_article, name='article_create')
    path('', IndexView.as_view(), name='index'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category'),
    path('article/<int:pk>/', ArticleDetail.as_view(), name='article'),
    path('create_article/', CreateArticle.as_view(), name='article_create'),
    path('article/<int:pk>/update/', UpdateArticle.as_view(), name='update'),
    path('article/<int:pk>/delete/', DeleteArticle.as_view(), name='delete'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('save_comment/<int:pk>/', save_comment, name='save_comment'),
    path('profile/<int:pk>/', profile, name='profile')
]