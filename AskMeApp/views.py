from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from re import findall, match, fullmatch
from AskMe.settings import enable_urls
from .models import Question
from .forms import LoginForm, QuestionForm


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
                        return HttpResponse('helo')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
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
    return render(request, 'signup.html')


@login_required
def settings(request):
    context = {'auth': 1}
    return render(request, 'settings.html', context)


@login_required
def ask(request):
    context = {'auth': 1}
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponse('Invalid login')
    else:
        form = QuestionForm()
        context.update({'form': form})
    return render(request, 'ask.html', context)


def questions(request):
    context = {'auth': 0}
    if request.user.is_authenticated:
        context['auth'] = 1

    questions_qs = Question.objects.get_new_questions()

    page = request.GET.get('page')
    posts = create_paginator(questions_qs, 20, page)

    context.update({'page': page})
    context.update({'posts': posts})
    context.update({'status': 1})
    return render(request, 'questions.html', context)


def question(request, question_id):
    context = {'auth': 0}
    if request.user.is_authenticated:
        context['auth'] = 1
    question_obj = Question.objects.get_question_by_id(question_id)
    answers_qs = Question.objects.get_new_answers(question_obj)

    page = request.GET.get('page')
    posts = create_paginator(answers_qs, 4, page)

    context.update({'question': question_obj})
    context.update({'page': page})
    context.update({'answers': posts})
    return render(request, 'question.html', context)


def tag(request, tag_name):
    context = {'auth': 0}
    if request.user.is_authenticated:
        context['auth'] = 1
    questions_qs = Question.objects.get_questions_by_tag(tag_name)

    page = request.GET.get('page')
    posts = create_paginator(questions_qs, 20, page)

    context.update({'page': page})
    context.update({'posts': posts})
    context.update({'status': 1})
    return render(request, 'questions.html', context)


def hot(request):
    context = {'auth': 0}
    if request.user.is_authenticated:
        context['auth'] = 1
    questions_qs = Question.objects.get_questions_by_rating()

    page = request.GET.get('page')
    posts = create_paginator(questions_qs, 20, page)

    context.update({'page': page})
    context.update({'posts': posts})
    context.update({'status': 0})
    return render(request, 'questions.html', context)
