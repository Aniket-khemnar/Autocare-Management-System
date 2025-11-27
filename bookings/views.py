from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ServiceBooking
from .serializers import BookingSerializer
from users.permissions import IsAdmin, IsMechanic, IsCustomer

User = get_user_model()


class BookingViewSet(viewsets.ModelViewSet):
    # ViewSet for managing bookings:
    # - Customers: create + view their own
    # - Mechanics: view + update assigned
    # - Admins: view all + assign mechanics

    queryset = ServiceBooking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Handle Swagger docs (important fix)
        if getattr(self, 'swagger_fake_view', False):
            return ServiceBooking.objects.none()
        
        if user.role == 'admin':
            return ServiceBooking.objects.all().order_by('-created_at')
        elif user.role == 'mechanic':
            return ServiceBooking.objects.filter(mechanic=user).order_by('-created_at')
        else:
            return ServiceBooking.objects.filter(customer=user).order_by('-created_at')

    def perform_create(self, serializer):
        user = self.request.user
        # Admin can create bookings for any user, others create for themselves
        if user.role == 'admin' and ('customer' in serializer.validated_data or 'customer_id' in serializer.validated_data):
            # Admin specified a customer (via customer_id which maps to customer), use that
            serializer.save()
        else:
            # Non-admin or admin didn't specify customer, use request.user
            serializer.save(customer=user)

    #  ADMIN: Assign Mechanic
    @action(detail=True, methods=['put'], permission_classes=[IsAdmin], url_path='assign')
    def assign(self, request, pk=None):
        booking = self.get_object()
        mechanic_id = request.data.get("mechanic_id")

        if not mechanic_id:
          return Response({"error": "mechanic_id required"}, status=400)

        mechanic = User.objects.get(id=mechanic_id, role="mechanic")

        booking.mechanic = mechanic
        booking.status = "in_progress"
        booking.save()

        return Response({"message": "Mechanic assigned successfully"}, status=200)



    # ✔ MECHANIC: Update Status
    @action(detail=True, methods=['patch'], permission_classes=[IsMechanic])
    def update_status(self, request, pk=None):
        booking = self.get_object()
        user = request.user

        if booking.mechanic != user:
            return Response(
                {'detail': 'This booking is not assigned to you.'},
                status=403
            )

        new_status = request.data.get('status')
        notes = request.data.get('notes', '')

        if new_status not in ['in_progress', 'completed', 'cancelled']:
            return Response({'detail': 'Invalid status.'}, status=400)

        booking.status = new_status

        if notes:
            booking.notes = (booking.notes or "") + f"\n[Update by {user.username}]: {notes}"

        booking.save()

        return Response(
            {'detail': f'Status updated to {new_status}.'},
            status=200
        )

    # ✔ MECHANIC: Dashboard summary feed (metrics + quick lists)
    @action(detail=False, methods=['get'], permission_classes=[IsMechanic], url_path='mechanic-summary')
    def mechanic_summary(self, request):
        user = request.user
        base_qs = ServiceBooking.objects.filter(mechanic=user)
        today = timezone.now().date()
        seven_days_ago = today - timedelta(days=7)

        next_job = base_qs.filter(preferred_date__gte=today).order_by('preferred_date').first()

        summary = {
            "counts": {
                "total_assigned": base_qs.count(),
                "active_jobs": base_qs.filter(status='in_progress').count(),
                "pending_jobs": base_qs.filter(status='pending').count(),
                "completed_week": base_qs.filter(
                    status='completed',
                    preferred_date__gte=seven_days_ago
                ).count(),
            },
            "next_job": BookingSerializer(next_job).data if next_job else None,
            "upcoming_jobs": BookingSerializer(
                base_qs.filter(status__in=['pending', 'in_progress'])
                .order_by('preferred_date')[:5],
                many=True
            ).data,
            "recent_activity": BookingSerializer(
                base_qs.order_by('-created_at')[:5],
                many=True
            ).data,
        }

        return Response(summary, status=200)
