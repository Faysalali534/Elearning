from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from .form import AddLessonForm, AddCourseForm, EditCourseForm, EditLessonForm
from .models import Course, Lesson, EnrollStudent


def group_required(group):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.filter(name=group).exists():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not autherized to access this page.")

        return wrapper_func

    return decorator


def course_detail(request, course):
    if request.user.is_authenticated:
        # lessons = Lesson.objects.filter(course=id).all()
        print('Course detail :', type(course))
        return render(request, 'learning_material/course_detail.html', {'course': course})


def all_courses_detail(request):
    if request.user.is_authenticated:
        courses = Course.objects.all()
        return render(request, 'learning_material/all_courses_detail.html', {'courses': courses})


class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(),
                                     self.get_login_url(), self.get_redirect_field_name())
        if not self.has_permission():
            return redirect('/')
        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)


class CourseEditView(UserAccessMixin, UpdateView):
    fields = ['course_id', 'name', 'description']
    raise_exception = False
    permission_required = 'learning_material.change_course'
    permission_denied_message = ''
    login_url = '/'
    redirect_field_name = 'next'

    model = Course
    form = EditCourseForm
    template_name = 'learning_material/edit_course.html'
    success_url = '/learning_material'

    def get_queryset(self, *args, **kwargs):
        queryset = Course.objects.filter(id=self.kwargs.get('pk'))
        res = Course.objects.filter(Q(id=queryset[0].id) & Q(taught_by=self.request.user.id))
        if not res:
            return res
        else:
            return queryset


class LessonEditView(UserAccessMixin, UpdateView):
    fields = ['lesson_id', 'name', 'created_at', 'course', 'created_by']
    raise_exception = False
    permission_required = 'learning_material.change_lesson'
    permission_denied_message = ''
    login_url = '/'
    redirect_field_name = 'next'

    model = Lesson
    form = EditLessonForm
    template_name = 'learning_material/edit_lesson.html'
    success_url = '/learning_material'


# Create your views here.
@method_decorator(login_required, name='dispatch')
class CourseListView(ListView):
    template_name = 'learning_material/course_list_view.html'
    context_object_name = 'courses'

    def get_queryset(self):
        queryset = Course.objects.filter(taught_by=self.request.user.id)
        return queryset


@login_required(login_url='login_request')
@group_required('professor')
def add_course(request):
    if request.method == "POST":
        course_form = AddCourseForm(data=request.POST)

        if course_form.is_valid():
            course = course_form.save(commit=False)
            course.taught_by = request.user
            course.save()
            return redirect('/learning_material')
        else:
            print(course_form.errors)
    else:
        course_form = AddCourseForm
    return render(request, 'learning_material/add_course.html', {'course_form': course_form})


@login_required(login_url='login_request')
@group_required('professor')
def add_lesson(request, course):
    registered = True

    if request.method == "POST":
        lesson_form = AddLessonForm(data=request.POST)

        if lesson_form.is_valid():
            lesson = lesson_form.save(commit=False)
            lesson.created_by = request.user
            lesson.course = Course.objects.filter(name__exact=course).get()
            lesson.save()
            return redirect('/learning_material')
        else:
            print(lesson_form.errors)
    else:
        lesson_form = AddLessonForm

    return render(request, 'learning_material/add_lesson.html',
                  {'registered': registered,
                   'lesson_form': lesson_form})


class CourseView(TemplateView):
    template_name = "learning_material/course_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.get(id=1)
        context['data'] = "Context Data for CourseView"
        return context


def professor_dashboard(request):
    courses = Course.objects.filter(taught_by=request.user.id)
    enroll_students_list = []
    for course in courses:
        enroll = EnrollStudent.objects.filter(course_id=course)
        enroll_students_list.append(enroll)
    return render(request, 'learning_material/base.html',
                  context={'enroll_students_list': enroll_students_list})


class EnrollStudentsView(TemplateView):
    template_name = "learning_material/enroll_students_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = Course.objects.get(name=self.kwargs.get('id'))
        enroll_stud = EnrollStudent.objects.filter(course_id=course_id).all()
        if enroll_stud:
            context['enrollStudents'] = enroll_stud
        else:
            context['enrollStudents'] = None
        return context


class CourseLessonView(TemplateView):
    template_name = "learning_material/course_lessons.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = Course.objects.get(name=self.kwargs.get('name'))
        context['lessons'] = Lesson.objects.filter(course_id=course_id)
        context['course'] = self.kwargs.get('name')
        return context


class ThanksTemplateView(TemplateView):
    template_name = 'learning_material/thanks.html'


def enroll_student(request, name):
    if request.user.is_authenticated:
        course_id = Course.objects.get(name=name)
        enroll, created = EnrollStudent.objects.get_or_create(student_id=request.user, course_id=course_id)
        if created:
            enroll.save()
        return render(request, 'learning_material/enroll_students_view.html', {})
