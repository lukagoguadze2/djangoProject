from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse(
        render(request, 'pages/index.html', context={})
    )


def contact(request):
    return render(request, 'pages/contact.html', {})
