from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from .form import UserForm, UserInfoForm, EditAccountForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.signals import request_finished
from django.dispatch import receiver


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


def logout_view(request):
    logout(request)
    return redirect('/')


def index_page(request):
    return render(request, 'accounts/index.html', {})


def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()

            profile = profile_form.save(commit=False)
            user_type = profile_form.cleaned_data['user_type']
            print(user_type)
            group_get, created = Group.objects.get_or_create(name=user_type)
            if not created:
                user.groups.add(group_get)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm
        profile_form = UserInfoForm

    return render(request, 'accounts/register.html',
                  {'registered': registered,
                   'user_form': user_form,
                   'profile_form': profile_form})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'accounts/login.html', context={'form': AuthenticationForm()})


@receiver(request_finished)
def my_callback(sender, **kwargs):
    print(sender, ' ', kwargs)
    print('Request Finished')


@anonymous_user
def view_profile(request):
    context = {'name': request.user.username}
    return render(request, 'accounts/profile.html', context)


@anonymous_user
def edit_profile(request):
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = EditAccountForm(instance=request.user)
        context = {'form': form}
        return render(request, 'accounts/edit_profile.html', context)
