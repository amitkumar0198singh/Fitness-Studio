

from booking.models import FitnessClass


def validate_request_data(required_fields, request_data):
    for field in required_fields:
        if field not in request_data:
            return {'status': False, 'message': f"{field} is required"}
    return {'status': True, 'message': "All required fields are present"}



def validate_slots(slots: int, fitness_class: FitnessClass) -> bool:
    return slots <= fitness_class.available_slots

