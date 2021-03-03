from django.conf.urls import url
from django.urls import path
from .import views

app_name = 'accounts'
urlpatterns = [
     path("", views.index_page, name='index'),
     path('accounts/register/', views.register, name='register'),
     path('accounts/login/', views.login_request, name='login_request'),
     path('accounts/logout/', views.logout_view, name='logout'),
     url(r"^accounts/profile/$", views.view_profile, name='view_profile'),
     url(r"^accounts/edit/$", views.edit_profile, name='edit_profile'),
]
