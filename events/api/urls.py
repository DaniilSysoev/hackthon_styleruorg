from django.urls import path, include
from rest_framework import routers
from .views import EventViewSet, BookingViewSet, ProfileRegistrationAPIView


router = routers.SimpleRouter()
router.register('event', EventViewSet, basename='event')
router.register('booking', BookingViewSet, basename='booking')


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/register/', ProfileRegistrationAPIView.as_view(), name='register'),
]