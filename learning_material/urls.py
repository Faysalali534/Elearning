from django.urls import path

from learning_material import views

app_name = 'learning_material'
urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('course_detail/<course>/', views.course_detail, name='course_detail'),
    path('course_view/', views.CourseView.as_view(), name='course_view'),
    path('all_courses_detail/', views.all_courses_detail, name='all_courses_detail'),
    path('enroll_course_list/<int:id>/', views.EnrollCoursesList.as_view(), name='enroll_course_list'),

    path('add_course/', views.add_course, name='add_course'),
    path('add_lesson/<course>/', views.add_lesson, name='add_lesson'),

    path('edit_course/<int:pk>/', views.CourseEditView.as_view(), name='edit_course'),
    path('edit_lesson/<int:pk>/', views.LessonEditView.as_view(), name='edit_lesson'),

    path('delete_course/<str:name>/', views.CourseDeleteView.as_view(), name='delete_course'),
    path('delete_lesson/<str:name>/<int:id>/', views.LessonDeleteView.as_view(), name='delete_lesson'),

    path('start_searching_course/', views.CourseSearchView.as_view(), name='start_searching_course'),
    path('info_list_view/', views.InfoListView.as_view(), name='info_list_view'),

    path('enroll_students_view/<str:id>/', views.EnrollStudentsView.as_view(), name='enroll_students_view'),
    path('enroll_student/<str:name>/', views.enroll_student, name='enroll_student'),
    path('course_lesson_view/<str:name>/', views.CourseLessonView.as_view(), name='course_lesson_view'),
    path('professor_dashboard/', views.professor_dashboard, name='professor_dashboard'),
    path("take_quiz/", views.take_quiz, name='take_quiz'),
]
