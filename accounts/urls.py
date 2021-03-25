from django.urls import path
from accounts import views

app_name = 'accounts'
urlpatterns = [
     path("", views.index_page, name='index'),
     path('accounts/register/', views.register, name='register'),
     path('accounts/login/', views.login_request, name='login_request'),
     path('accounts/logout/', views.logout_view, name='logout'),
     path("accounts/profile/", views.profile_view, name='profile_view'),
     path("accounts/edit/", views.edit_profile, name='edit_profile'),

     path("set/", views.set_session, name='set_session'),
     path("get/", views.get_session, name='get_session'),
     path("del/", views.del_session, name='del_session'),
]
