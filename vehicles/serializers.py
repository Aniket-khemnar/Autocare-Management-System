from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Vehicle

User = get_user_model()


class VehicleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Vehicle
        fields = [
            'id',
            'user',
            'user_id',
            'username',
            'model',
            'registration_no',
            'last_service_date',
            'mileage',
            'next_service_due'
        ]
