from allauth.account.views import LoginView
from django.urls import path

class CustomLoginView(LoginView):
    template_name = 'account/login.html'  # Use your custom template if needed

# In your urls.py
urlpatterns += [
    path('api/auth/login/', CustomLoginView.as_view(), name='account_login'),
]