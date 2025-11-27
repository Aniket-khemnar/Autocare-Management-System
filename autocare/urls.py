from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="AutoCare API",
        default_version='v1',
        description="API documentation for AutoCare",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


from users.urls import api_urlpatterns as users_api_urls, html_urlpatterns as users_html_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include(users_api_urls)),      # Creates: /api/auth/login/, /api/auth/register/, /api/token/refresh/, /api/users/
    path('api/vehicles/', include('vehicles.urls')),  # Creates: /api/vehicles/
    path('api/', include('bookings.urls')),   # Creates: /api/bookings/
    path('api/reminders/', include('reminders.urls')),  # Creates: /api/reminders/

    # HTML Pages (separate from API routes)
    path('', include(users_html_urls)),  # Creates: /, /login/, /register/, /dashboard/
    path('dashboard/', include('dashboard.urls')),  # Dashboard pages

    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
