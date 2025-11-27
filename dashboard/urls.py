from django.urls import path
from . import views
from .views import admin_dashboard, mechanic_dashboard, customer_dashboard
from .views import manage_users, manage_vehicles, manage_bookings

urlpatterns = [
    path("admin/", admin_dashboard, name="admin_dashboard"),
    path("mechanic/", mechanic_dashboard, name="mechanic_dashboard"),
    path("customer/", customer_dashboard, name="customer_dashboard"),

    path("admin/manage-users/", views.manage_users, name="manage_users"),
    path("admin/manage-vehicles/", views.manage_vehicles, name="manage_vehicles"),
    path("admin/manage-bookings/", views.manage_bookings, name="manage_bookings"),

    path('add-vehicle/', views.add_vehicle_page, name='add_vehicle'),
    path('book-service/', views.book_service_page, name='book_service'),
    path('edit-vehicle/<int:vehicle_id>/', views.edit_vehicle_page, name='edit_vehicle_page'),
]
