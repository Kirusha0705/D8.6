from django.urls import path
from .views import PostsList, PostDetail, PostDelete, ArticleCreate, ArticleUpdate, ArticleDetail

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>', ArticleDetail.as_view(), name='article_detail'),
   #path('search', PostList2.as_view()),
   path('create/', ArticleCreate.as_view(), name='article_create'),
   path('<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]