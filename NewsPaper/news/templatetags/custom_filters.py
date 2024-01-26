from django import template

register = template.Library()

FORBIDDEN_WORDS = (
    'редиска',
    'вторжения',
    'тайнопись',
    'маск',
    'маска',
    'маском'
)


@register.filter()
def censor(value):
    if isinstance(value, str):
        words = value.split()
        result = ''
        for word in words:
            if word.isalpha():
                if word.lower() in FORBIDDEN_WORDS:
                    result += ' ' + word[:1] + '*' * (len(word) - 1)
                else:
                    result += f' {word}'
            else:
                if word.lower()[:-1] in FORBIDDEN_WORDS:
                    result += ' ' + word[:1] + '*' * (len(word) - 2) + word[-1]
        return result
    else:
        raise ValueError


@register.filter()
def get_url(value):
    if value == 'News':
        return 'news'
    if value == 'Article':
        return 'articles'
