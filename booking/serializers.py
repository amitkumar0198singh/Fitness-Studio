from rest_framework import serializers
from booking.models import FitnessClass, Booking




class FitnessClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = FitnessClass
        exclude = ['max_slots', 'is_active']


class BookingSerializer(serializers.ModelSerializer):
    fitness_class = serializers.CharField(source='fitness_class.name', read_only=True)
    class Meta:
        model = Booking
        fields = '__all__'