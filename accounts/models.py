from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserInfoManager(models.Manager):
    def get_queryset(self, ):
        return super(UserInfoManager, self).get_queryset().filter(location='liberty gate')

    def get_professor(self, prof):
        return super(UserInfoManager, self).get_queryset().filter(user_name__contains=prof)


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    phone_number = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    student = 'student'
    professor = 'professor'
    user_types = [
        (student, 'student'),
        (professor, 'professor'),
    ]
    user_type = models.CharField(max_length=9, choices=user_types, default=student)

    objects = models.Manager()
    liberty = UserInfoManager()

    def __str__(self):
        return self.user.username


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


models.signals.pre_save.connect(set_username, sender=User)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)
        print(sender)
        print(kwargs)
        print("Post save working")
