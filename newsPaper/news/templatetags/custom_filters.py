from django import template
from news.censorwords import CENSOR


register = template.Library()

@register.filter()
def censor(value: str):
    censored = ''
    for item in value.split():
        if item.lower() in CENSOR:
            cen_item = item[0] + '*' * (len(item) - 1)
            censored += cen_item + ' '
        else:
            censored += item + ' '
    return censored
