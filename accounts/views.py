from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from accounts.form import UserForm, UserProfileForm, EditAccountForm, EditUserInfoForm
from accounts.decorators import anonymous_user


def logout_view(request):
    logout(request)
    return redirect('/')


def index_page(request):
    return render(request, 'accounts/index.html', {})


def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()

            profile = profile_form.save(commit=False)
            user_type = profile_form.cleaned_data['user_type']
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
        profile_form = UserProfileForm

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


@anonymous_user
def profile_view(request):
    session_visits_limit(request)
    context = {'name': request.user.username}
    return render(request, 'accounts/profile.html', context)


@anonymous_user
def edit_profile(request):
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        userinfo_form = EditUserInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            user_form = form.save()
            custom_form = userinfo_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('profile_view')
    else:
        form = EditAccountForm(instance=request.user)
        custom_form = EditUserInfoForm(instance=request.user)
        context = {'form': form, 'custom_form': custom_form}
        return render(request, 'accounts/edit_profile.html', context)


def set_session(request):
    request.session['notification'] = 'Test'
    return render(request, 'learning_material/setsession.html')


def get_session(request):
    test = request.session.get('notification')
    return render(request, 'learning_material/getsession.html', {'test': test})


def del_session(request):
    if 'notification' in request.session:
        del request.session['notification']
    return render(request, 'learning_material/delsession.html')


def session_visits_limit(request):
    num_visits = request.session.get('num_visits', 0) + 1
    request.session['num_visits'] = num_visits
    if num_visits > 4:
        del (request.session['num_visits'])
        request.session.flush()
    return HttpResponse('view count=' + str(num_visits))
