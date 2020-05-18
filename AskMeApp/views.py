import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import urlencode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from re import fullmatch

from django.views import View

from AskMe.settings import enable_urls
from .models import Question, Like
from .forms import LoginForm, QuestionForm, AnswerForm, SettingsForm, RegisterForm


def create_paginator(data, elements_in_page, page):
    paginator = Paginator(data, elements_in_page)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)
    return posts


def is_enable_url(some_url):
    for url in enable_urls:
        enable_url = r'/AskMe/' + url
        if fullmatch(enable_url, some_url):
            return True
    return False


def index(request):
    return HttpResponse('hello')


def sign_in(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('ask_me:questions'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    next_page = request.POST.get('next', '/')
                    if is_enable_url(next_page):
                        return HttpResponseRedirect(next_page)
                    else:
                        return HttpResponse('Bad page')
                else:
                    return HttpResponse('Disabled account')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def sign_out(request):
    logout(request)
    next_page = request.GET.get('next', '/')
    return HttpResponseRedirect(next_page)


def sign_up(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('ask_me:questions'))
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            user = form.save()
            user_au = authenticate(username=cd['username'], password=cd['password'])
            login(request, user_au)
            return HttpResponseRedirect(reverse('ask_me:questions'))
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'signup.html', context)


@login_required
def settings(request):
    context = {}
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            return HttpResponseRedirect(reverse('ask_me:questions'))
    else:
        form = SettingsForm(instance=request.user)
    context.update({'form': form})
    return render(request, 'settings.html', context)


@login_required
def ask(request):
    context = {}
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('ask_me:question', question_id=post.id)
    else:
        form = QuestionForm()
    context.update({'form': form})
    return render(request, 'ask.html', context)


def questions(request):
    context = {}

    questions_qs = Question.objects.get_new_questions()

    page = request.GET.get('page')
    posts = create_paginator(questions_qs, 20, page)

    context.update({'page': page})
    context.update({'posts': posts})
    context.update({'status': 1})
    return render(request, 'questions.html', context)


def question(request, question_id):
    context = {}

    question_obj = Question.objects.get_question_by_id(question_id)
    print(question_obj.rating)
    answers_qs = Question.objects.get_new_answers(question_obj)

    page = request.GET.get('page')
    posts = create_paginator(answers_qs, 4, page)

    if request.user.is_authenticated:
        context.update({'user': request.user})
        if request.method == 'POST':
            form = AnswerForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                post = form.save(commit=False)
                post.author = request.user
                post.question = question_obj
                post.save()
                question_obj.answers_count += 1
                question_obj.save()
                # как это сделать лучше?
                get_args_str = urlencode({'page': 1})
                url = '/AskMe/question/' + str(question_obj.id) + '/?' + get_args_str
                return HttpResponseRedirect(url)
        else:
            form = AnswerForm()
        context.update({'form': form})

    context.update({'question': question_obj})
    context.update({'page': page})
    context.update({'answers': posts})
    return render(request, 'question.html', context)


def tag(request, tag_name):
    context = {}

    questions_qs = Question.objects.get_questions_by_tag(tag_name)

    page = request.GET.get('page')
    posts = create_paginator(questions_qs, 20, page)

    context.update({'page': page})
    context.update({'posts': posts})
    context.update({'status': 1})
    return render(request, 'questions.html', context)


def hot(request):
    context = {}
    questions_qs = Question.objects.get_questions_by_rating()

    page = request.GET.get('page')
    posts = create_paginator(questions_qs, 20, page)

    context.update({'page': page})
    context.update({'posts': posts})
    context.update({'status': 0})
    return render(request, 'questions.html', context)


class VotesView(View):
    model = None  # Модель вопроса или ответа
    vote_type = None  # Лайк или дизлайк

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        try:
            like_dislike = Like.objects.get(content_type=ContentType.objects.get_for_model(obj),
                                            object_id=obj.id,
                                            user=request.user)

            # если оценка пользователя на этот объект отличается от поставленной ранее
            # меняем оценку и рейтинг
            if like_dislike.vote is not self.vote_type:
                like_dislike.vote = self.vote_type
                obj.rating += 2 * self.vote_type
                like_dislike.save(update_fields=['vote'])
                result = True
            # если совпадает - отменяем предыдущую оценку,
            # обновляем рейтинг, удаляем модель лайка
            else:
                obj.rating -= self.vote_type
                like_dislike.delete()
                result = False
        # если ранне оценок не было создаем модель лайка и обновляем рейтинг
        except Like.DoesNotExist:
            obj.likes.create(user=request.user, vote=self.vote_type)
            obj.rating += self.vote_type
            result = True

        obj.save()
        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.likes.likes().count(),
                "dislike_count": obj.likes.dislikes().count(),
            }),
            content_type="application/json"
        )
