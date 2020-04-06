from django.conf.urls import url
from . import views


app_name = 'ask_me'
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^auth/$', views.authorisation, name='auth'),
    url(r'^unauth/$', views.unauthorisation, name='unauth'),
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.sing_up, name='sing_up'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^ask/$', views.ask, name='ask'),
    url(r'^$', views.questions, name='questions'),
    url(r'^question/(?P<question_id>\d+)/$', views.question, name='question'),
    url(r'^hot/$', views.hot, name='hot'),
]