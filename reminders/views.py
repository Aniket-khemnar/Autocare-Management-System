from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from bookings.models import ServiceBooking
from datetime import date, timedelta


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def run_reminders(request):
    """
    Finds bookings scheduled for tomorrow and triggers reminders (simulated).
    """
    tomorrow = date.today() + timedelta(days=1)
    upcoming = ServiceBooking.objects.filter(preferred_date=tomorrow)

    count = upcoming.count()

    # Example of actual reminder logic (placeholder)
    # for booking in upcoming:
    #     send_email(booking.customer.email, "Reminder", "You have a booking tomorrow!")

    return Response({
        "status": "success",
        "checked_date": str(tomorrow),
        "reminders_sent": count,
        "message": f"Reminders triggered for {count} bookings scheduled for tomorrow."
    })
