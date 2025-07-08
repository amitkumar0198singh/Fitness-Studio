from datetime import datetime

from django.db.models import QuerySet

from booking import custom_exception
from booking.models import FitnessClass, Booking
from booking.validators import validate_slots



def get_class_by_id(class_id: int) -> FitnessClass:
    try:
        return FitnessClass.objects.get(id=class_id)
    except FitnessClass.DoesNotExist:
        raise custom_exception.DataNotFoundException("Please choose a valid fitness class")

def get_classes() -> QuerySet[FitnessClass]:
    return FitnessClass.objects.filter(is_active=True, class_time__gt=datetime.now()).order_by('-class_time')




def get_all_bookings() -> QuerySet[Booking]:
    return Booking.objects.all().order_by('-booking_time')


def booking_create_or_update(name: str, email: str, fitness_class: FitnessClass, slots: int) -> Booking:
    booking, _ = Booking.objects.update_or_create(client_email=email, fitness_class=fitness_class, defaults={'client_name': name})
    booking.booked_slots += slots
    booking.save()
    return booking

def book_class(name: str, email: str, class_id: int|str, slots: int|str|None = None) -> Booking:
    fitness_class = get_class_by_id(int(class_id))
    slots = int(slots) if slots else 1
    is_available_slots = validate_slots(slots, fitness_class)
    if not is_available_slots:
        raise custom_exception.DataNotFoundException("Slots are not available")
    booking = booking_create_or_update(name, email, fitness_class, slots)
    fitness_class.available_slots -= slots
    fitness_class.save()
    return booking