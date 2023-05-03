from rest_framework import serializers
from .models import Event, Booking
from django.contrib.auth import get_user_model


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'date')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('event_id', 'user_id')


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email', 'telegram',  'first_name', 'last_name', 'is_staff')
        extra_kwargs = {'password': {'write_only': True}}


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')