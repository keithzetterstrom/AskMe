from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Question, Answer

# Create your views here.

# questions_dct = {
#     i: {'id': i, 'title': f'question # {i}', 'text': f'text ))) {i}'}
#     for i in range(5)
# }

questions_dct = [
    {'id': 0, 'title': f'question # 0', 'text': f'text ))) 0', 'like': 1, 'data': '22.02.2020'},
    {'id': 1, 'title': f'question # 1', 'text': f'text ))) 1', 'like': 2, 'data': '22.02.2020'},
    {'id': 2, 'title': f'question # 2', 'text': f'text ))) 2', 'like': 4, 'data': '22.02.2020'},
    {'id': 3, 'title': f'question # 3', 'text': f'text ))) 3', 'like': 7, 'data': '22.02.2020'},
    {'id': 4, 'title': f'question # 4', 'text': f'text ))) 4', 'like': 11, 'data': '22.02.2020'},
    {'id': 5, 'title': f'question # 5', 'text': f'text ))) 5', 'like': 0, 'data': '22.02.2020'},
    {'id': 6, 'title': f'question # 6', 'text': f'text ))) 6', 'like': 6, 'data': '22.02.2020'},
]


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


def login(request):
    return render(request, 'login.html')


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
               'posts': posts}
    return render(request, 'questions.html', context)


def question(request, question_id):
    question_obj = get_object_or_404(Question, pk=question_id)
    answers_qs = question_obj.answer_set.all()

    page = request.GET.get('page')
    posts = create_paginator(answers_qs, 5, page)

    context = {'dct': question_obj,
               'answers': posts,
               'page': page}
    return render(request, 'question.html', context)


def tag(request, tag_id):
    questions_qs = Question.objects.get_questions_by_tag(tag_id)

    page = request.GET.get('page')
    posts = create_paginator(questions_qs, 20, page)

    context = {'page': page,
               'posts': posts}
    return render(request, 'questions.html', context)
