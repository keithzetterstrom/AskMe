import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import urlencode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.views import View
from .models import Question, Like, Answer
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


def index(request):
    return HttpResponse('hello')


def sign_in(request):
    # если пользователь авторизован, вернуть его на страницу вопросов
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('ask_me:questions'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            # проверяем, есть ли такой пользователь
            if user is not None:
                if user.is_active:
                    # авторизируем пользователя
                    login(request, user)
                    next_page = request.POST.get('next', '/')
                    return HttpResponseRedirect(next_page)
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
    # если пользователь авторизован, вернуть его на страницу вопросов
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
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            return HttpResponseRedirect(reverse('ask_me:questions'))
    else:
        form = SettingsForm(instance=request.user)
    context = {'form': form}
    return render(request, 'settings.html', context)


@login_required
def ask(request):
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
    context = {'form': form}
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
    answers_qs = Question.objects.get_new_answers(question_obj)

    page = request.GET.get('page')
    posts = create_paginator(answers_qs, 4, page)

    # если пользователь авторизован, отобразить форму для ответа
    if request.user.is_authenticated:
        context.update({'user': request.user})
        if request.method == 'POST':
            form = AnswerForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                # сохраняем с условием, что некоторые поля будут добавлены позже
                post = form.save(commit=False)
                # добавляем автора ответа
                post.author = request.user
                # добавляем вопрос на который написан ответ
                post.question = question_obj
                post.save()
                #question_obj.answers_count += 1
                question_obj.save()
                # берем страницу пагинатора ответов для редиректа на созданный ответ
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
    questions_qs = Question.objects.get_questions_by_rating

    page = request.GET.get('page')
    posts = create_paginator(questions_qs, 20, page)

    context.update({'page': page})
    context.update({'posts': posts})
    context.update({'status': 0})
    return render(request, 'questions.html', context)


def correct_answer(request, pk):
    answer_obj = Answer.objects.get(pk=pk)
    if request.user != answer_obj.question.author:
        return HttpResponse('Disabled account')
    prev_answer_id = -1
    # если ответ изначально не был выбран как правильный
    # ставим ему отметку True
    if not answer_obj.correct_mark:
        answer = Answer.objects.get_correct_answer(answer_obj.question.id)
        # проверяем, есть ли другой ответ, выбранный как верный
        # если да, убираем отметку и запоминаем id этого ответа
        if answer:
            answer[0].correct_mark = False
            answer[0].save()
            prev_answer_id = answer[0].id
        answer_obj.correct_mark = True
    # если изначально был выбран верным, снимаем эту отметку
    else:
        answer_obj.correct_mark = False

    answer_obj.save()
    return HttpResponse(
            json.dumps({
                "prev_answer_id": prev_answer_id,
            }), content_type="application/json")


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
                like_dislike.save(update_fields=['vote'])
                obj.rating += 2 * self.vote_type
                result = True
            # если совпадает - отменяем предыдущую оценку,
            # обновляем рейтинг, удаляем модель лайка
            else:
                like_dislike.delete()
                obj.rating -= self.vote_type
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
                "rating": obj.rating,
            }),
            content_type="application/json"
        )
