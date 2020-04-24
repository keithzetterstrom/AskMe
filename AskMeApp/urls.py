from django.conf.urls import url
from . import views


app_name = 'ask_me'
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^login/$', views.sign_in, name='login'),
    url(r'^signup/$', views.sign_up, name='sign_up'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^ask/$', views.ask, name='ask'),
    url(r'^$', views.questions, name='questions'),
    url(r'^question/(?P<question_id>\d+)/$', views.question, name='question'),
    url(r'^tag/(?P<tag_name>[^/]+)/$', views.tag, name='tag'),
    url(r'^hot/$', views.hot, name='hot'),
    url(r'^logout/$', views.sign_out, name='logout'),
]
