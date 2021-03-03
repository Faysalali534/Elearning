from django.contrib.auth.signals import user_logged_in


@user_logged_in
def login_success():
    print('Logged In Signal')
