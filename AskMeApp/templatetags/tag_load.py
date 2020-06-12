from django.core.cache import cache
from django import template

register = template.Library()


@register.inclusion_tag('tag_output.html')
def show_results():
    tags = cache.get('top100_tags')
    if tags:
        return {'tags': tags[:20]}
    return {'tags': tags}
