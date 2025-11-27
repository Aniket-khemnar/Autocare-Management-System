from rest_framework import serializers
from .models import ServiceBooking
from vehicles.serializers import VehicleSerializer
from vehicles.models import Vehicle
from django.contrib.auth import get_user_model

User = get_user_model()

class BookingSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        required=False,
        source='customer'
    )

    # For READ — nested full vehicle details
    vehicle = VehicleSerializer(read_only=True)

    # For WRITE — only vehicle_id is required
    vehicle_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(),
        write_only=True,
        source='vehicle'
    )

    mechanic = serializers.SerializerMethodField()
    mechanic_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, required=False, source='mechanic'
    )

    class Meta:
        model = ServiceBooking
        fields = [
            'id',
            'customer',
            'customer_id',   # write only PK field (for admin to create bookings for others)
            'vehicle',       # read only nested object
            'vehicle_id',    # write only PK field
            'service_type',
            'preferred_date',
            'status',
            'notes',
            'admin_notes',
            'mechanic',
            'mechanic_id',
            'created_at',
        ]
        read_only_fields = ['created_at']

    def get_customer(self, obj):
        return {
            "id": obj.customer.id,
            "username": obj.customer.username,
            "email": obj.customer.email,
        }

    def get_mechanic(self, obj):
        if obj.mechanic:
            return {
                "id": obj.mechanic.id,
                "username": obj.mechanic.username
            }
        return None
