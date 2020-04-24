from django.contrib.auth import authenticate, login
from django.db.models import Count, Sum
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Question, Answer
from .forms import LoginForm


def create_paginator(data, elements_in_page, page):
    paginator = Paginator(data, elements_in_page)  # поста на каждой странице
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)
    return posts


def index(request):
    return HttpResponse('hello')


def authorisation(request):
    return render(request, 'base.html', {'auth': 1})


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
                    return HttpResponseRedirect(next_page)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def sign_up(request):
    return render(request, 'signup.html')


def settings(request):
    return render(request, 'settings.html')


def ask(request):
    return render(request, 'ask.html')


def questions(request):
    questions_qs = Question.objects.get_new_questions()

    page = request.GET.get('page')
    posts = create_paginator(questions_qs, 20, page)

    context = {'page': page,
               'posts': posts,
               'status': 1}
    return render(request, 'questions.html', context)


def question(request, question_id):
    question_obj = Question.objects.get_question_by_id(question_id)
    answers_qs = question_obj.answer_set.all().annotate(rating=Sum('likes_answer__vote'))

    page = request.GET.get('page')
    posts = create_paginator(answers_qs, 4, page)
    print(question_obj.tags)

    context = {'question': question_obj,
               'answers': posts,
               'page': page}
    return render(request, 'question.html', context)


def tag(request, tag_id):
    questions_qs = Question.objects.get_questions_by_tag(tag_id)
    print(questions_qs[1].rating)

    page = request.GET.get('page')
    posts = create_paginator(questions_qs, 20, page)

    context = {'page': page,
               'posts': posts,
               'status': 0}
    return render(request, 'questions.html', context)


def hot(request):
    questions_qs = Question.objects.get_questions_by_rating()

    page = request.GET.get('page')
    posts = create_paginator(questions_qs, 20, page)

    context = {'page': page,
               'posts': posts,
               'status': 0}
    return render(request, 'questions.html', context)
