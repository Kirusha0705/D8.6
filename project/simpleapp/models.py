from django.db import models
from django.urls import reverse
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class Post(models.Model):
    article = models.CharField(
        max_length=50,
    )
    text = models.TextField()
    time_in = models.DateTimeField(
        auto_now_add=True
    )
    name_author = models.TextField()


    def __str__(self):
        return f'{self.article.title()}: {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )



