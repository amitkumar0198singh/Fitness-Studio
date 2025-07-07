from django.urls import path
from booking.views import UpcomingClassesView, BookingView, BookingsView


urlpatterns = [
    path('classes/', UpcomingClassesView.as_view(), name='upcoming-classes'),
    path('book/', BookingView.as_view(), name='booking'),
    path('bookings/', BookingsView.as_view(), name='bookings'),
]