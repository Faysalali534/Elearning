from django.urls import path, include
# from rest_framework.authtoken.views import obtain_auth_token
from restapi.auth import CustomAuthToken
from restapi import views
from rest_framework.routers import DefaultRouter


app_name = 'restapi'
router = DefaultRouter()


router.register('userapi', views.UserModelViewSet, basename='user')


urlpatterns = [
     path('', include(router.urls)),
     # path('google/', views.GoogleSocialAuthView.as_view()),
     path('gettoken/', CustomAuthToken.as_view()),
     path('login_api_view/', views.LoginApiView.as_view(), name='login_api_view'),
     path("user_profile_result/", views.user_profile_result, name='user_profile_result'),
     path("profile_create/", views.create_user_profile, name='profile_create'),
     path("profile_get/<int:pk>/", views.get_user_profile, name='profile_get'),
     path("user_api/<int:pk>/", views.UserAPI.as_view(), name='user_api'),
     path("update_user/", views.update_user, name='update_user'),
     path("delete_user/", views.delete_user, name='delete_user'),
     path('user_profile_api/', views.UserProfileAPI.as_view(), name='user_profile_api'),
     path('user_list_api/', views.UserListAPI.as_view(), name='user_list_api'),
     path('user_create_api/', views.UserCreateAPI.as_view(), name='user_create_api'),
     path('user_retrieve_api/<int:pk>/', views.UserRetrieveAPI.as_view(), name='user_retrieve_api'),
     path('list_create_api_view/', views.UserListCreateAPIView.as_view(), name='list_create_api_view'),
     path('retrieve_update_destroy_api_view/<int:pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view(),
          name='retrieve_update_destroy_api_view'),
]
