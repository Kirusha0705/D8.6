from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView
)
from datetime import datetime
from django.views.generic import ListView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .models import BaseRegisterForm
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class PostDetail(DeleteView):
    model = Post
    template_name = 'news2.html'
    context_object_name = 'news'


class PostList2(ListView):
    model = Post
    ordering = '-article'
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 5

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_news'] = None
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = 'simpleapp.add_post'

    def form_valid(self, form):
        news = form.save(commit=False)
        news._type = 'NE'
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin,  LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
    permission_required = 'simpleapp.add_post'

    def form_valid(self, form):
        article = form.save(commit=False)
        article._type = 'AR'
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = 'simpleapp.change_post'


class ArticleUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
    permission_required = 'simpleapp.change_post'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class ArticleDetail(DeleteView):
    model = Post
    template_name = 'article2.html'
    context_object_name = 'news'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'



