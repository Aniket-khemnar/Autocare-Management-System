from rest_framework import serializers
from .models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    
    class Meta:
        model = Vehicle
        fields = ['id', 'user', 'user_id', 'username', 'model', 'registration_no', 'last_service_date', 'mileage', 'next_service_due']
