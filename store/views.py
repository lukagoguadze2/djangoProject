from django.http import JsonResponse


def index(request):
    return JsonResponse({'message': 'This is the store page!'})
