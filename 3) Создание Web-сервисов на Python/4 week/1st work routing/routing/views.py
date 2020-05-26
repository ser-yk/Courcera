from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_http_methods, require_POST

# @require_http_methods(['GET', 'PUT', 'POST'])
def simple_route(request, something):
    method = request.method
    if method == 'GET' and not something:
        return HttpResponse(status=200, content='')
    elif method in ('POST', 'PUT'):
        return HttpResponse(status=405)
    else:
        return HttpResponse(status=404)


def slug_route(request, slug):
    if slug:
        return HttpResponse(status=200, content=slug)
    else:
        return HttpResponse(status=404)


def sum_route(request, arg1, arg2):
    try:
        arg1, arg2 = int(arg1), int(arg2)
        return HttpResponse(status=200, content=arg1 + arg2)
    except ValueError:
        return HttpResponse(status=404)


def sum_get_method(request):
    if request.method == 'GET':
        try:
            a = int(request.GET.get('a'))
            b = int(request.GET.get('b'))
            return HttpResponse(status=200, content=a + b)
        except:
            return HttpResponse(status=400)
    return HttpResponse(status=405)


def sum_post_method(request):
    if request.method == 'POST':
        try:
            a = int(request.POST.get('a'))
            b = int(request.POST.get('b'))
            return HttpResponse(status=200, content=a + b)
        except:
            return HttpResponse(status=400)
    return HttpResponse(status=405)
