from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.signals import set_username


class UserInfoManager(models.Manager):
    def get_queryset(self, ):
        return super(UserInfoManager, self).get_queryset().filter(location='liberty gate')

    def get_professor(self, prof):
        return super(UserInfoManager, self).get_queryset().filter(username__contains=prof)


AUTH_PROVIDERS = {
    'google': 'google', 'email': 'email'
}


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    student = 'student'
    professor = 'professor'
    # auth_provider = models.CharField(
    #     max_length=100, blank=True, null=True,
    #     default=AUTH_PROVIDERS.get('email')
    # )
    user_types = [
        (student, 'student'),
        (professor, 'professor'),
    ]
    user_type = models.CharField(max_length=9, choices=user_types, default=student)

    objects = models.Manager()
    liberty = UserInfoManager()

    def __str__(self):
        return self.user.username

    # def tokens(self):
    #     refresh = RefreshToken.for_user(self)
    #     return {
    #         'refresh': str(refresh),
    #         'access': str(refresh.access_token)
    #     }


models.signals.pre_save.connect(set_username, sender=User)


class Test(models.Model):
    my_time = models.DateTimeField(default=timezone.now)


class GenQuerySet:
    start = 1
    p = 0
    offset = 0
    chunk = 10
    convert = ''
    __instance__ = None

    @staticmethod
    def getInstance():
        if GenQuerySet.__instance__ is None:
            GenQuerySet()
        return GenQuerySet.__instance__

    def __init__(self):
        if GenQuerySet.__instance__:
            raise Exception('Singleton')
        else:
            GenQuerySet.__instance__ = self

    @classmethod
    def gen_queryset(cls, queryset, chunk=10):
        if cls.p == 100:
            cls.start += 1
            cls.p = 0

        if cls.start % 2 == 1:
            cls.convert = 'pst'
        else:
            cls.convert = 'utc'
        print(cls.p, ' ', cls.p + chunk)
        while True:
            items = queryset.all().values('pk')[cls.p:cls.p+chunk]
            print(items)
            if not items:
                break
            cls.p += chunk
            return cls.convert, items


def ordered_results():
    test = Test.objects.all().order_by('id')
    return test


def get():
    test = ordered_results()
    g = GenQuerySet.getInstance()
    conversion, item = g.gen_queryset(test)
    print('Converting in ', conversion)
    # for user in item:
    return conversion, item
