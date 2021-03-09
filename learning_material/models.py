from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
    course_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    taught_by = models.ForeignKey("auth.User", limit_choices_to={'groups__name': "professor"}, on_delete=models.Empty,
                                  related_name='taught_by', null=True, blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    lesson_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey("auth.User", limit_choices_to={'groups__name': "professor"},
                                   on_delete=models.CASCADE,
                                   related_name='createdBy', null=True, blank=True)
    created_at = models.DateTimeField(default=now, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    class Meta:
        ordering = ['lesson_id']

    def __str__(self):
        return self.name


class EnrollStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey('auth.User', limit_choices_to={'groups__name': 'student'}
                                   , on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    enrolled_at = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return self.student_id.username


def set_course_taught_by(sender, instance, user, **kwargs):
    print(sender)
    print(kwargs)
    print('reciver :', user.username)
    if not instance.taught_by:
        username = instance.first_name
        counter = 1
        while User.objects.filter(username=username):
            username = instance.first_name + str(counter)
            counter += 1
        instance.username = username

# models.signals.pre_save.connect(set_course_taught_by, sender=Course)
