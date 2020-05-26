from django.shortcuts import render
from django.http import HttpResponse


def echo(request):
    method = request.method
    meta = request.META.get('HTTP_X_PRINT_STATEMENT') or 'empty'
    string = ''
    if method == 'POST':
        for k, v in request.POST.items():
            string = f'{method.lower()} {k}: {v} statement is {meta}'
        return render(request, r'echo.html', {'string': string})
    elif method == 'GET':
        for k, v in request.GET.items():
            string = f'{method.lower()} {k}: {v} statement is {meta}'
        return render(request, r'echo.html', {'string': string})


def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 1),
        'b': request.GET.get('b', 1)
    })


def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })
