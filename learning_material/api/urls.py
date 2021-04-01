from django.urls import path, include
# from rest_framework.authtoken.views import obtain_auth_token
from restapi.auth import CustomAuthToken
from learning_material.api import views
from rest_framework.routers import DefaultRouter

app_name = 'api'
router = DefaultRouter()

router.register('course_lesson_api', views.CourseLessonApiViewSet, basename='course_lesson')
router.register('course_info_api', views.CourseInfoViewSet, basename='course_info')
router.register('lesson_api', views.LessonViewSet, basename='lesson_info')
router.register('enroll_student_api', views.EnrollStudentViewSet, basename='enroll_student')
router.register('enroll_in_course_api', views.EnrollUserViewSet, basename='enroll_in_course')
urlpatterns = [
     path('', include(router.urls)),
     path('gettoken/', CustomAuthToken.as_view()),
]


# urlpatterns = [
#      path("user_profile_result/", views.user_profile_result, name='user_profile_result'),
#      path("user_enroll_result/", views.user_enroll_result, name='user_enroll_result'),
#      path("profile_create/", views.create_user_profile, name='profile_create'),
#      path("profile_get/<int:pk>/", views.get_user_profile, name='profile_get'),
#      path("user_api/<int:pk>/", views.UserAPI.as_view(), name='user_api'),
#      path("update_user/", views.update_user, name='update_user'),
#      path("delete_user/", views.delete_user, name='delete_user'),
#      path('user_profile_api/', views.UserProfileAPI.as_view(), name='user_profile_api'),
#      path('user_list_api/', views.UserListAPI.as_view(), name='user_list_api'),
#      path('user_create_api/', views.UserCreateAPI.as_view(), name='user_create_api'),
#      path('user_retrieve_api/<int:pk>/', views.UserRetrieveAPI.as_view(), name='user_retrieve_api'),
#      path('list_create_api_view/', views.UserListCreateAPIView.as_view(), name='list_create_api_view'),
#      path('retrieve_update_destroy_api_view/<int:pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view(),
#           name='retrieve_update_destroy_api_view'),
# ]
