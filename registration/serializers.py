from rest_framework import serializers
from .models import CustomUser


class DataSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name']

class ClientRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only= True)
    class Meta:
        model = CustomUser
        fields = ['id', 'password', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user

# class DriverRegistrationSerializer(serializers.ModelSerializer):
#     first_name = serializers.CharField(max_length=30)
#     last_name = serializers.CharField(max_length=30)
#     password = serializers.CharField(write_only= True)
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'password', 'first_name', 'last_name', 'email']

#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(
#             first_name = validated_data['first_name'],
#             last_name = validated_data['last_name'],
#             email = validated_data['email'],
#             password = validated_data['password']
#         )
#         return user

class DriverUpdateSerializer(serializers.ModelSerializer):
    is_driver = serializers.BooleanField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['is_driver', 'phone_no']

