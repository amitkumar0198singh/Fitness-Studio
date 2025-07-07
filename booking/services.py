from datetime import datetime

from booking.models import FitnessClass, Booking
from booking.validators import validate_slots



def get_class_by_id(fitness_class_id):
    try:
        return FitnessClass.objects.get(id=fitness_class_id)
    except FitnessClass.DoesNotExist:
        return None

def get_classes():
    return FitnessClass.objects.filter(is_active=True, class_time__gt=datetime.now()).order_by('-class_time')


def get_all_bookings():
    return Booking.objects.all().order_by('-booking_time')


def book_class(name: str, email: str, fitness_class: FitnessClass, slots: int|str|None = None):
    slots = int(slots) if slots else 1
    is_available_slots = validate_slots(slots, fitness_class)
    if not is_available_slots:
        return None
    booking = Booking.objects.create(client_name=name, client_email=email, fitness_class=fitness_class)
    fitness_class.available_slots -= slots
    fitness_class.save()
    return booking