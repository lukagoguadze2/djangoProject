from django.conf import settings
from django.urls import resolve, Resolver404


def pages(request):
    path = request.path.strip('/').split('/')

    pages_ = []

    breadcrumb_url = ''

    for part in path:
        breadcrumb_url += '/' + part
        try:
            resolve(breadcrumb_url + "/")  # თუ არსებობს ეს URL მაშინ დავამატოთ
            pages_.append({
                'name': part.capitalize(),
                'href': breadcrumb_url
            })
        except Resolver404:
            pass

    return {
        'current_page': path[-1].capitalize(),
        'pages': pages_
    }


def website_name(request):
    return {
        'WEBSITE_NAME': settings.WEBSITE_NAME
    }
