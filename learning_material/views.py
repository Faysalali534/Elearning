from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .form import AddLessonForm, AddCourseForm
from .models import Course, Lesson


def group_required(group):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.filter(name=group).exists():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not autherized to access this page.")
        return wrapper_func
    return decorator


def course_detail(request, id):
    if request.user.is_authenticated:
        lessons = Lesson.objects.filter(course__pk=id).all()
        return render(request, 'learning_material/course_lessons.html', {'lessons': lessons})


# Create your views here.
@method_decorator(login_required, name='dispatch')
class CourseListView(ListView):
    template_name = 'learning_material/course_list_view.html'
    model = Course
    context_object_name = 'courses'


@login_required(login_url='login_request')
@group_required('professor')
def add_course(request):
    if request.method == "POST":
        course_form = AddCourseForm(data=request.POST)

        if course_form.is_valid():
            course_form.save()
            return redirect('/learning_material')
        else:
            print(course_form.errors)
    else:
        course_form = AddCourseForm
    return render(request, 'learning_material/add_course.html', {'course_form': course_form})


@login_required(login_url='login_request')
@group_required('professor')
def add_lesson(request):
    registered = True

    if request.method == "POST":
        lesson_form = AddLessonForm(data=request.POST)

        if lesson_form.is_valid():
            lesson_id = lesson_form.cleaned_data['lesson_id']
            name = lesson_form.cleaned_data['name']
            created_at = lesson_form.cleaned_data['created_at']
            course = lesson_form.cleaned_data['course']
            lesson_form.save()
            return redirect('/learning_material')
        else:
            print(lesson_form.errors)
    else:
        lesson_form = AddLessonForm

    return render(request, 'learning_material/add_lesson.html',
                  {'registered': registered,
                   'lesson_form': lesson_form})
