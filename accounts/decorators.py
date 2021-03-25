from django.shortcuts import redirect
from django.http import Http404


def group_required(group):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.filter(name=group).exists():
                return view_func(request, *args, **kwargs)
            else:
                return Http404("You are not authorized to access this page.")
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
            return Http404("You are not logged In.")
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
