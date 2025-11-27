from rest_framework import viewsets
from .models import Vehicle
from .serializers import VehicleSerializer
from rest_framework.permissions import IsAuthenticated

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # For Swagger fake view
        if getattr(self, 'swagger_fake_view', False):
            return Vehicle.objects.none()

        # Not authenticated → return nothing
        if not user.is_authenticated:
            return Vehicle.objects.none()

        # Base queryset based on role
        if user.role == 'admin':
            queryset = Vehicle.objects.all()
        elif user.role == 'mechanic':
            queryset = Vehicle.objects.filter(assigned_mechanic=user)
        else:  # customer
            queryset = Vehicle.objects.filter(user=user)

        # ---- NEW PART: Filtering by user ID (Admin only) ----
        user_id = self.request.query_params.get('user')
        if user.role == 'admin' and user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user

        # Admin can set user manually
        if user.role == 'admin' and 'user' in serializer.validated_data:
            serializer.save()
        else:
            serializer.save(user=user)

    def perform_update(self, serializer):
        user = self.request.user

        # Admin can update everything
        if user.role == 'admin':
            serializer.save()
        else:
            # Non-admin user cannot update other user's vehicles
            serializer.save()
