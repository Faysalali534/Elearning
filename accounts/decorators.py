from django.http import HttpResponse
from django.shortcuts import redirect


def group_required(group):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.filter(name=group).exists():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not autherized to access this page.")
        return wrapper_func
    return decorator


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def anonymous_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_anonymous:
            return HttpResponse("You are not logged In.")
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
