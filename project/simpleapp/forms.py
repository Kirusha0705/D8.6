from django.forms import DateInput
from django_filters import FilterSet, DateFilter
from django import forms
from .models import Post
from datetime import datetime
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = ['article', 'text', 'name_author']

    def clean(self):
        cleaned_data = super().clean()
        article = cleaned_data.get("article")
        text = cleaned_data.get("text")

        if text == article:
            raise ValidationError(
                "Текст статьи не может быть идентичен названию."
            )

        return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
