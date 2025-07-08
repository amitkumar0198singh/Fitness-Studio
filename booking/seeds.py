from datetime import datetime, timedelta

from .models import FitnessClass


def run():
    FitnessClass.objects.all().delete()
    now = datetime.now()
    class_data = [
        {"name": "Yoga", "instructor": "Priya Sharma", "max_slots": 20, "available_slots": 20, "class_time": now + timedelta(days=3)},
        {"name": "Zumba", "instructor": "Rahul Verma", "max_slots": 15, "available_slots": 15, "class_time": now + timedelta(days=5)},
        {"name": "HIIT", "instructor": "Anjali Patel", "max_slots": 10, "available_slots": 10, "class_time": now + timedelta(days=9)}
    ]
    FitnessClass.objects.bulk_create([FitnessClass(**entry) for entry in class_data])
    print(f"Seeded {len(class_data)} fitness classes.")

