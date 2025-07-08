from datetime import datetime, timedelta

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from booking.models import FitnessClass, Booking


class FitnessBookingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test fitness classes
        self.fitness_class = FitnessClass.objects.create(
            name="Yoga",
            instructor="Priya Sharma",
            max_slots=10,
            available_slots=10,
            class_time=datetime.now() + timedelta(days=1),
        )

        self.valid_payload = {
            "client_name": "Amit Kumar",
            "client_email": "amit@example.com",
            "class_id": self.fitness_class.id,
            "slots": 2
        }

    def test_get_classes(self):
        response = self.client.get('/classes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('classes', response.data)
        self.assertGreaterEqual(len(response.data['classes']), 1)

    def test_successful_booking(self):
        response = self.client.post('/book/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], True)
        self.assertEqual(Booking.objects.count(), 1)

    def test_booking_with_missing_email(self):
        payload = {
            "client_name": "Amit",
            "class_id": self.fitness_class.id
        }
        response = self.client.post('/book/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], "client_email is required")

    def test_booking_with_excess_slots(self):
        payload = {
            "client_name": "Amit",
            "client_email": "amit@example.com",
            "class_id": self.fitness_class.id,
            "slots": 99  # Exceeds available slots
        }
        response = self.client.post('/book/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "Data not found")

    def test_get_bookings_by_email_success(self):
        # Book a class
        self.client.post('/book/', self.valid_payload, format='json')

        # Fetch booking
        response = self.client.get('/bookings/', {'email': 'amit@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['bookings']), 1)
        self.assertEqual(response.data['bookings'][0]['client_email'], 'amit@example.com')

    def test_get_bookings_by_email_not_found(self):
        response = self.client.get('/bookings/', {'email': 'nonexistent@example.com'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], "Data not found")

    def test_get_bookings_without_email(self):
        response = self.client.get('/bookings/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['detail'], "Client email is required")
