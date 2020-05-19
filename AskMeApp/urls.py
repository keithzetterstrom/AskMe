from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from .models import Like, Question, Answer
from .views import VotesView

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
    url(r'^js/question/(?P<pk>\d+)/like/$',
        VotesView.as_view(model=Question, vote_type=Like.LIKE), name='question_like'),
    url(r'^js/question/(?P<pk>\d+)/dislike/$',
        login_required(VotesView.as_view(model=Question, vote_type=Like.DISLIKE)), name='question_dislike'),
    url(r'^js/answer/(?P<pk>\d+)/like/$', login_required(VotesView.as_view(model=Answer, vote_type=Like.LIKE)),
        name='answer_like'),
    url(r'^js/answer/(?P<pk>\d+)/dislike/$',
        login_required(VotesView.as_view(model=Answer, vote_type=Like.DISLIKE)), name='answer_dislike'),
    url(r'^js/answer/(?P<pk>\d+)/correct/$',
        login_required(views.correct_answer), name='answer_correct'),
]
