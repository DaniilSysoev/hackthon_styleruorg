from django.contrib import admin
from .models import Event, Booking


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'user_id')