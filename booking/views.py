from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from booking import custom_exception
from booking.serializers import BookingSerializer, FitnessClassSerializer
from booking.services import book_class, get_all_bookings, get_classes
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
        client_booking_data = book_class(
            name=requested_data.get('client_name'), email=requested_data.get('client_email'),
            class_id=requested_data.get('class_id'), slots=requested_data.get('slots')
        )
        client_booking_serializer = BookingSerializer(client_booking_data)
        return Response({'status': True, 'message': "Fitness class is booked", 'booking': client_booking_serializer.data}, status=status.HTTP_200_OK)

    
    @action(detail=False, methods=['get'], url_path='bookings', name='list_bookings')
    def list_bookings(self, request):
        client_booking_queryset = get_all_bookings().filter(client_email=request.data.get('client_email'))
        if not client_booking_queryset.exists():
            raise custom_exception.DataNotFoundException("No bookings found")
        client_booking_serializer = BookingSerializer(client_booking_queryset, many=True)
        return Response({'status': True, 'message': "Bookings are fetched", 'bookings': client_booking_serializer.data}, status=status.HTTP_200_OK)
