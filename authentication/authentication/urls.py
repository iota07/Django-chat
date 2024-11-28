"""
URL configuration for authentication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import CustomLoginView, CustomConfirmEmailView

# Swagger configuration
schema_view = get_schema_view(
    openapi.Info(
        title="PULP API",
        default_version='v1',
        description="API documentation PULP project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="service01.hm@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # Custom login view (if you have custom logic for login)
    path('api/auth/login/', CustomLoginView.as_view(), name='custom_login'),
    
    # Dj-rest-auth URLs for login, registration, password reset, etc.
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    
    # Custom email confirmation view (to return JSON instead of HTML)
    
    # **Override the default email confirmation URL** to use allauth
    # This makes sure that allauth handles the email confirmation logic
    path('api/auth/registration/account-confirm-email/<str:key>/', include('allauth.urls')),  # Let allauth handle email confirmation
    
    # Swagger UI documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
