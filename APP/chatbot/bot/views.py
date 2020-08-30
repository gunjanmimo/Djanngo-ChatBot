from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    context = {'a': 'hello world'}
    return render(request, 'chat.html', context)


def getResponse(request):
    if request.method == 'POST':
        print(" this is a post method")
        msg = request.POST.get('message')
        print(msg)

    context = {'a': 'hello world'}
    return render(request, 'chat.html', context)
