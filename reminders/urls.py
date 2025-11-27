from django.urls import path
from .views import run_reminders

urlpatterns = [
    path('run/', run_reminders, name='run-reminders'),
]
