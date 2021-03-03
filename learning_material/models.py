from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
    course_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    lesson_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='createdBy', null=True, blank=True)
    created_at = models.DateTimeField(default=now, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    class Meta:
        ordering = ['lesson_id']

    def __str__(self):
        return self.name

