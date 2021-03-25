from django.contrib import admin

from learning_material.models import Course, Lesson
# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'course_id', 'name', 'description'
    )


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)
