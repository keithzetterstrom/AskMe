from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

def index(request):
    return HttpResponse('hello')


def authorisation(request):
    return render(request, 'base_authorised.html')


def unauthorisation(request):
    return render(request, 'base_unauthorised.html')


def login(request):
    return render(request, 'login.html')


def sing_up(request):
    return render(request, 'signup.html')


def settings(request):
    return render(request, 'settings.html')


def ask(request):
    return render(request, 'ask.html')


def questions(request):
    paginator = Paginator(questions_dct, 3)  # 3 поста на каждой странице
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)

    return render(request, 'questions.html', {'page': page, 'posts': posts})


def question(request, question_id):

    return render(request, 'question.html', {'dct': questions_dct[int(question_id)]})


def hot(request):
    return render(request, 'questions.html')