from django.http import JsonResponse, HttpResponse
import requests
import json


def index(request):
    response = requests.get('https://fakestoreapi.com/products')
    return JsonResponse(data=response.json(), status=response.status_code, safe=False)


def item(request, _id):
    if request.method == "GET":
        response = requests.get(f'https://fakestoreapi.com/products/{int(_id)}')
        if response.status_code == 200 and response.content:
            return JsonResponse(data=response.json(), status=response.status_code, safe=False)
        else:
            return JsonResponse(data={'message': 'item not found!'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def display_component(request, _id, component):
    if request.method == "GET":
        response = item(request, _id)

        component = component.lower()
        request_path = "/".join(request.path.split('/')[:-1])

        json_ = json.loads(response.content)
        keys = [
            f'<li><a href="{request_path + '/' + key}">{key}</a></li>' for key in list(json_.keys())
        ]

        if response.status_code == 200 and component in json_.keys():
            html_content = f"""
                <html>
                    <head><title>My Page</title></head>
                    <body>
                        <h1>{component.capitalize()}</h1>
                        {f'<img src="{json_["image"]}">' if component == 'image' else ''}
                        <p>{json_[component]}</p>
                        <br>
                        <strong>See also</strong>
                            <ul>{''.join(keys)}</ul>
                    </body>
                </html>
                """
            return HttpResponse(html_content, content_type='text/html')

        else:
            if 'message' in json_.keys():
                return HttpResponse("<h1>Item not found!</h1>", status=404)
            else:
                return HttpResponse("<h1>Component not found!</h1>"
                                "<strong>Valid Components are:</strong>"
                                f"<ul>{''.join(keys)}</ul>", status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
