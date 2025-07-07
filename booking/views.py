from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from booking.models import Booking, FitnessClass
from booking.serializers import BookingSerializer, FitnessClassSerializer
from booking.services import book_class, get_all_bookings, get_class_by_id, get_classes
from booking.validators import validate_request_data


# Create your views here.

class FitnessClassBookView(viewsets.ViewSet):

    @action(detail=False, methods=['get'], url_path='classes', name='get_fitness_classes')
    def get_fitness_classes(self, request):
        fitness_classes_queryset = get_classes()
        fitness_classes_serializer = FitnessClassSerializer(fitness_classes_queryset, many=True)
        return Response({
            'status': True, 'message': "Fitness classes are fetched", 'classes': fitness_classes_serializer.data
        }, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['post'], url_path='book', name='book_fitness_class')
    def book_fitness_class(self, request):
        requested_data = request.data
        required_fields = ['client_name', 'client_email', 'class_id']
        validation_response = validate_request_data(required_fields, requested_data)
        if not validation_response.get('status'):
            return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
        fitness_class = get_class_by_id(requested_data.get('class_id'))
        if not fitness_class:
            return Response({'status': False, 'message': "Please choose a valid fitness class"}, status=status.HTTP_404_NOT_FOUND)
        if not fitness_class.is_active:
            return Response({'status': False, 'message': "This fitness class is not active"}, status=status.HTTP_400_BAD_REQUEST)
        client_booking_data = book_class(
            name=requested_data.get('client_name'), email=requested_data.get('client_email'),
            fitness_class=fitness_class, slots=requested_data.get('slots')
        )
        if not client_booking_data:
            return Response({'status': False, 'message': "Slots are not available"}, status=status.HTTP_400_BAD_REQUEST)
        client_booking_serializer = BookingSerializer(client_booking_data)
        return Response({'status': True, 'message': "Fitness class is booked", 'booking': client_booking_serializer.data}, status=status.HTTP_200_OK)

    
    @action(detail=False, methods=['get'], url_path='bookings', name='list_bookings')
    def list_bookings(self, request):
        client_booking_queryset = get_all_bookings().filter(client_email=request.data.get('email'))
        if not client_booking_queryset.exists():
            return Response({'status': False, 'message': "No bookings found"}, status=status.HTTP_404_NOT_FOUND)
        client_booking_serializer = BookingSerializer(client_booking_queryset, many=True)
        return Response(client_booking_serializer.data, status=status.HTTP_200_OK)




# class FitnessClassView(APIView):
#     def get(self, request):
#         fitness_classes = FitnessClass.objects.filter(is_active=True, class_time__gt=datetime.now()).order_by('-class_time')
#         fitness_classes_serializer = FitnessClassSerializer(fitness_classes, many=True)
#         return Response(fitness_classes_serializer.data, status=status.HTTP_200_OK)
    

# class ListBookingsView(APIView):
#     def get(self, request):
#         client_booking_queryset = Booking.objects.filter(client_email=request.data.get('email'))
#         if not client_booking_queryset.exists():
#             return Response({'status': False, 'message': "No bookings found"}, status=status.HTTP_404_NOT_FOUND)
#         client_booking_serializer = BookingSerializer(client_booking_queryset, many=True)
#         return Response(client_booking_serializer.data, status=status.HTTP_200_OK)
    

# class CreateBookingView(APIView):
#     def post(self, request):
#         client_booking = Booking.objects.create(client_name=request.data.get('name'), client_email=request.data.get('email'), fitness_class=request.data.get('class_id'))
#         client_booking_serializer = BookingSerializer(client_booking)
#         return Response(client_booking_serializer.data, status=status.HTTP_200_OK)