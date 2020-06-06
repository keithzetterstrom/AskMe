from AskMeApp.models import User
from django import template

register = template.Library()


@register.inclusion_tag('users_output.html')
def show_users():
    users = list(User.objects.order_by('-rating').values_list('username', flat=True)[:5])
    return {'users': users}
