from django.urls import path
from .import views

app_name = 'learning_material'
urlpatterns = [
     path('', views.CourseListView.as_view(), name='course_list'),
     path('course_detail/<str:id>/', views.course_detail, name='course_detail'),
     path('add_course/', views.add_course, name='add_course'),
     path('add_lesson/', views.add_lesson, name='add_lesson'),
]
