from django.conf.urls import url
from . import views

app_name = 'ask_me'
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^auth/$', views.authorisation, name='auth'),
    url(r'^unauth/$', views.unauthorisation, name='unauth'),
    url(r'^login/$', views.login, name='login'),

]