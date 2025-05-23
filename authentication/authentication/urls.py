from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from allauth.account.views import confirm_email
from .views import CustomLoginView

# Swagger configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Intranet HM Service API",
        default_version='v1.2',
        description="API documentation HM Intranet project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="service01.hm@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Authentication URLs
    path('api/auth/login/', CustomLoginView.as_view(), name='custom_login'),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    re_path(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('accounts/', include('allauth.urls')),

    # Intranet app URLs (all viewsets and API endpoints)
    path('api/intranet/', include('intranet.urls')),

    # Swagger and API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]