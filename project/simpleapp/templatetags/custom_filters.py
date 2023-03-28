from django import template

register = template.Library()

bad_words = ['простак', 'дурак', 'псина']


@register.filter()
def censor(value):
    for word in bad_words:
        if word in value:
            censor_word = ''.join(['*' for word in range(len(word))])
            value = value.replace(word, censor_word)
    return value



