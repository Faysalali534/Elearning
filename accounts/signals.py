from django.contrib.auth.models import User


def set_username(sender, instance, **kwargs):
    print(sender)
    print(kwargs)
    if not instance.username:
        username = instance.first_name
        counter = 1
        while User.objects.filter(username=username):
            username = instance.first_name + str(counter)
            counter += 1
        instance.username = username
