from rest_framework import serializers
from .models import Event, Booking
from django.contrib.auth import get_user_model


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title', 'description', 'date')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('event_id', 'user_id')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}