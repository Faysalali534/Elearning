from django import forms
from .models import Lesson, Course


class AddCourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = (
            'course_id',
            'name',
            'description',
        )


class AddLessonForm(forms.ModelForm):

    class Meta:
        model = Lesson
        fields = (
            'lesson_id',
            'name',
            'created_by',
            'created_at',
            'course',
        )
