from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from allauth.account.views import ConfirmEmailView
from authentication.views import CustomLoginView

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
    
    # Custom login view
    path('api/auth/login/', CustomLoginView.as_view(), name='custom_login'),
    
    # Dj-rest-auth URLs for login, registration, password reset, etc.
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    
    # Custom email confirmation view
    path('api/auth/registration/account-confirm-email/<str:key>/', 
         ConfirmEmailView.as_view(), 
         name='account_confirm_email'),
    
    # Swagger UI documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]