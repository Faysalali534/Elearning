from django import forms
from django.contrib.auth.forms import UserChangeForm

from .models import Lesson, Course


class AddCourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = (
            'course_id',
            'name',
            'description',
        )


class EditCourseForm(UserChangeForm):
    course_id = forms.CharField(required=True)
    name = forms.CharField(required=True)
    description = forms.CharField(required=True)

    class Meta:
        model = Course
        fields = [
            'course_id',
            'name',
            'description',
        ]


class AddLessonForm(forms.ModelForm):

    class Meta:
        model = Lesson
        fields = (
            'lesson_id',
            'name',
            'created_at',
        )


class EditLessonForm(UserChangeForm):
    lesson_id = forms.CharField(required=True)
    name = forms.CharField(required=True)
    created_at = forms.DateTimeField(required=True)
    course = forms.ChoiceField(required=True)

    class Meta:
        model = Lesson
        fields = [
            'lesson_id',
            'name',
            'created_at',
            'course'
        ]