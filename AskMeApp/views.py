from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

questions = {
    i: {'id': i, 'title': f'question # {i}'}
    for i in range(5)
}


def index(request):
    return HttpResponse('hello')


def authorisation(request):
    return render(request, 'base_authorised.html')


def unauthorisation(request):
    return render(request, 'base_unauthorised.html')


def login(request):
    return render(request, 'login.html')