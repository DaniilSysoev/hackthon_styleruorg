from rest_framework import serializers
from .models import Event, Booking
from django.contrib.auth import get_user_model


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title', 'description', 'date', 'image')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('event_id', 'user_id')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user