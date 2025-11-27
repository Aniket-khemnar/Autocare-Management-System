from django.shortcuts import render
from django.contrib.auth import get_user_model
from vehicles.models import Vehicle
from bookings.models import ServiceBooking

User = get_user_model()


def admin_dashboard(request):
    total_users = User.objects.count()
    total_mechanics = User.objects.filter(role="mechanic").count()
    total_customers = User.objects.filter(role="customer").count()

    total_vehicles = Vehicle.objects.count()
    total_bookings = ServiceBooking.objects.count()

    pending_bookings = ServiceBooking.objects.filter(status="pending").count()
    in_progress_bookings = ServiceBooking.objects.filter(status="in_progress").count()
    completed_bookings = ServiceBooking.objects.filter(status="completed").count()

    context = {
        "total_users": total_users,
        "total_mechanics": total_mechanics,
        "total_customers": total_customers,
        
        "total_vehicles": total_vehicles,
        "total_bookings": total_bookings,

        "pending_bookings": pending_bookings,
        "in_progress_bookings": in_progress_bookings,
        "completed_bookings": completed_bookings,
    }

    return render(request, "dashboard/admin_dashboard.html", context)

def customer_dashboard(request):
    return render(request, "dashboard/customer_dashboard.html")

def mechanic_dashboard(request):
    return render(request, "dashboard/mechanic_dashboard.html")



def manage_users(request):
    users = User.objects.all()
    return render(request, "dashboard/admin_manage_users.html", {"users": users})



def manage_vehicles(request):
    vehicles = Vehicle.objects.all()
    return render(request, "dashboard/admin_manage_vehicles.html", {"vehicles": vehicles})

def manage_bookings(request):
    bookings = ServiceBooking.objects.select_related("customer", "vehicle","mechanic").all()
    context = {
        "bookings": bookings
    }
    return render(request, "dashboard/admin_manage_bookings.html", context)


def add_vehicle_page(request):
    return render(request, 'dashboard/add_vehicle.html')

def book_service_page(request):
    return render(request, 'dashboard/book_service.html')

def edit_vehicle_page(request, vehicle_id):
    return render(request, 'dashboard/edit_vehicle.html', {'vehicle_id': vehicle_id})