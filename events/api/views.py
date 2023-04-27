from rest_framework import viewsets, permissions
from .models import Event, Booking
from .serializers import EventSerializer, BookingSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.utils import timezone


class ProfileRegistrationAPIView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                return Response({'token': token.key}, status=201)
        return Response(serializer.errors, status=400)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAdminUser,)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        #взять айди пользователя по токену авторизации, взять айди события из запроса и создать бронь
        user = Token.objects.get(key=request.auth.key).user
        event = Event.objects.get(id=request.data['event_id'])
        if event.date < timezone.now():
            return Response('Вы не можете забронировать прошедшее событие', status=400)
        if Booking.objects.filter(event_id=event, user_id=user).exists():
            return Response('Вы уже забронировали это событие', status=400)
        request.data['user_id'] = user.id
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return None
    
    def retrieve(self, request, *args, **kwargs):
        return None
    
    def update(self, request, *args, **kwargs):
        return None
    
    def partial_update(self, request, *args, **kwargs):
        return None
    
    def destroy(self, request, *args, **kwargs):
        return None