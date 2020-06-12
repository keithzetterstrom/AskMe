from django.core.cache import cache
from django import template

register = template.Library()


@register.inclusion_tag('users_output.html')
def show_users():
    users = cache.get('top100_users')
    if users:
        return {'users': users[:5]}
    return {'users': users}
