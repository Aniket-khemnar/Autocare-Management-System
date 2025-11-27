from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt

from . import views
from .views import (
    RegisterView, 
    LoginView, 
    register_page, 
    login_page, 
    UserViewSet
)

from rest_framework_simplejwt.views import TokenRefreshView


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

# API URL patterns (included at /api/ in root urls.py)
# These create: /api/auth/login/, /api/auth/register/, /api/token/refresh/, /api/users/
api_urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='api_register'),
    path('auth/login/', csrf_exempt(LoginView.as_view()), name='api_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),  # Creates /api/users/
]

# HTML URL patterns (included at root level)
# These create: /, /login/, /register/
html_urlpatterns = [
    path("", views.home_page, name="home"),
    path("register/", register_page, name="register_page"),
    path("login/", login_page, name="login_page"),
]

# Default export (for backward compatibility)
urlpatterns = html_urlpatterns
