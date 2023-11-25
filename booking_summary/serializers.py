from rest_framework import serializers
from .models import BookingSummary, Junction, Ride, PriceTable, Car

# from django.conf import settings


# CustomUser = settings.AUTH_USER_MODEL

from django.contrib.auth import get_user_model  # Add this import

User = get_user_model() 

class BookingSummarySerializer (serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    distance = serializers.FloatField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = BookingSummary
        fields = ['user', 'user_location', 'destination', 'two_way', 'no_of_passengers', 'pickup_long', 'pickup_lat', 'dest_long', 'dest_lat', 'distance', 'price', 'created_at']


class JunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Junction
        fields = ['id', 'name', 'created', 'updated']

class PriceTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceTable
        fields = ['id', 'start_junction', 'end_junction', 'price', 'created', 'updated']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class RideSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    start_junction = JunctionSerializer()
    end_junction = JunctionSerializer()
    class Meta:
        model = Ride
        fields = ['user','id', 'start_junction', 'end_junction', 'no_of_passengers', 'two_way', 'price', 'created']


class UserRideSerializer(serializers.ModelSerializer):
    start_junction = JunctionSerializer()
    end_junction = JunctionSerializer()
    class Meta:
        model = Ride
        fields = ['id', 'start_junction', 'end_junction', 'no_of_passengers', 'two_way', 'price', 'created']


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'car_model', 'license_plate','driver']