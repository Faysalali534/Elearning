import json
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.base import TemplateView, View
from django.shortcuts import render, redirect, get_object_or_404


from learning_material.form import AddLessonForm, AddCourseForm, EditCourseForm, EditLessonForm, SearchCourseForm
from learning_material.models import Course, Lesson, EnrollStudent


def group_required(group):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.filter(name=group).exists():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to access this page.")

        return wrapper_func

    return decorator


def course_detail(request, course):
    if request.user.is_authenticated:
        return render(request, 'learning_material/course_detail.html', {'course': course})


def all_courses_detail(request):
    if request.user.is_authenticated:
        courses = EnrollStudent.objects.filter(student_id=request.user.id).values('course_id_id')
        id_list = []
        for course in courses:
            id_list.append(course['course_id_id'])
        courses = Course.objects.exclude(id__in=id_list)
        return render(request, 'learning_material/all_courses_detail.html', {'courses': courses})


class EnrollCoursesList(ListView):
    template_name = 'learning_material/enroll_course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        courses = EnrollStudent.objects.filter(student_id=self.kwargs.get('id')).values('course_id_id')
        id_list = []
        for course in courses:
            id_list.append(course['course_id_id'])
        queryset = Course.objects.filter(id__in=id_list).all()
        return queryset


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
class CourseListView(TemplateView):
    template_name = 'learning_material/course_list_view.html'

    def get(self, request):
        courses = Course.objects.filter(taught_by=self.request.user.id)
        form = SearchCourseForm()
        return render(request, self.template_name, {'courses': courses, 'form': form})

    def post(self, request, **kwargs):
        form = SearchCourseForm(self.request.POST)
        if form.is_valid():
            text = form.cleaned_data['name']
            courses = Course.objects.filter(taught_by=self.request.user.id).filter(name=text)
            return render(request, self.template_name, {'courses': courses, 'form': form})

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
            messages.success(request, 'Lesson Added Successfully.')
            return redirect('/learning_material')
        else:
            print(lesson_form.errors)
    else:
        lesson_form = AddLessonForm

    return render(request, 'learning_material/add_lesson.html',
                  {'registered': registered,
                   'lesson_form': lesson_form,
                   'messages': messages})


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
    return render(request, 'base.html',
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

    def get(self, request, name):
        course_id = Course.objects.get(name=self.kwargs.get('name'))
        lessons = Lesson.objects.filter(course_id=course_id)
        form = SearchCourseForm()
        return render(request, self.template_name, {'course': course_id, 'lessons': lessons, 'form': form})

    def post(self, request, **kwargs):
        form = SearchCourseForm(self.request.POST)
        if form.is_valid():
            text = form.cleaned_data['name']
            course_id = Course.objects.get(name=self.kwargs.get('name'))
            lessons = Lesson.objects.filter(course_id=course_id).filter(name=text)
            form = SearchCourseForm()
            return render(request, self.template_name, {'course': course_id, 'lessons': lessons, 'form': form})


def search(request):
    search_form = SearchCourseForm
    return render(request, 'learning_material/search_courses.html',
                  {'search_form': search_form})


class CourseSearchView(TemplateView):
    template_name = 'learning_material/search_courses.html'

    def get(self, request):
        form = SearchCourseForm()
        courses = Course.objects.all()
        return render(request, self.template_name, {'courses': courses, 'form': form})

    def post(self, request):
        form = SearchCourseForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['name']
            courses = Course.objects.filter(name=text)
            if not courses:
                form = SearchCourseForm()
                courses = None
                return render(request, self.template_name, {'courses': courses, 'form': form})
            else:
                args = {'courses': courses, 'form': form}
                return render(request, self.template_name, args)
        else:
            form = SearchCourseForm()
            courses = None
            return render(request, self.template_name, {'courses': courses, 'form': form})


class CourseDeleteView(View):
    template_name = 'learning_material/delete_course.html'

    def get(self, request, name):
        course = get_object_or_404(Course, name__iexact=name)
        return render(request, self.template_name, {'course': course})

    def post(self, request, name):
        course = get_object_or_404(Course, name__iexact=name)
        course.delete()
        return redirect(reverse('learning_material:course_list'))


class LessonDeleteView(View):
    template_name = 'learning_material/delete_lesson.html'

    def get(self, request, name, id):
        lesson = get_object_or_404(Lesson, id=id)
        return render(self.request, self.template_name, {'lesson': lesson})

    def post(self, request, name, id):
        lesson = get_object_or_404(Lesson, id=id)
        lesson.delete()
        return redirect(reverse('learning_material:course_lesson_view', args=(name,)))


def enroll_student(request, name):
    if request.user.is_authenticated:
        course_id = Course.objects.get(name=name)
        enroll, created = EnrollStudent.objects.get_or_create(student_id=request.user, course_id=course_id)
        if created:
            enroll.save()
        return render(request, 'learning_material/enroll_students_view.html', {})


def session_expiry(request):
    request.session.set_expiry(30)
    return render(request, 'learning_material/take_quiz.html')


def take_quiz(request):
    session_expiry(request)
    return render(request, 'learning_material/thanks.html')


class InfoListView(ListView):
    model = Course
    template_name = 'learning_material/search_course.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qs_json'] = json.dumps(list(Course.objects.values()))
        return context
