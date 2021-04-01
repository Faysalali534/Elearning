"""demo_register URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# import debug_toolbar

from django.urls import path, include
# from django.conf import settings
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='E-learning API Documentation')

urlpatterns = [
    path('', include('accounts.urls')),
    path('api_documentation/', schema_view),
    path('learning_material/', include('learning_material.urls')),
    path('restapi/', include('restapi.urls')),
    path('learning_material_api/', include('learning_material.api.urls')),
    path('admin/', admin.site.urls),
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh_token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('verify_token/', TokenVerifyView.as_view(), name='verify_token'),
]

# if settings.DEBUG:
#     urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
