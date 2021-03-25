from django.urls import path
from restapi import views

app_name = 'restapi'
urlpatterns = [
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
]
