from rest_framework import viewsets, permissions
from .models import Event, Booking
from .serializers import EventSerializer, BookingSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class ProfileRegistrationAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    User = get_user_model()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if the user with the given username already exists
        username = serializer.validated_data['username']
        if self.User.objects.filter(username=username).exists():
            return Response({'error': 'User with this username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the new user
        user = serializer.save()

        # Create a token for the new user
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_201_CREATED)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAdminUser,)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticated,)