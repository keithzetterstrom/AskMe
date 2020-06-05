from AskMeApp.models import Tag
from django import template

register = template.Library()


@register.inclusion_tag('tag_output.html')
def show_results():
    tags = list(Tag.objects.order_by('-questions_count').values_list('tag_name', flat=True)[:20])
    return {'tags': tags}
