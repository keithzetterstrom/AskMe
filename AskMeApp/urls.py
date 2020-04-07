from django.conf.urls import url
from . import views


app_name = 'ask_me'
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^auth/$', views.authorisation, name='auth'),
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.sign_up, name='sign_up'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^ask/$', views.ask, name='ask'),
    url(r'^$', views.questions, name='questions'),
    url(r'^question/(?P<question_id>\d+)/$', views.question, name='question'),
    url(r'^tag/$', views.tag, name='hot'),
]