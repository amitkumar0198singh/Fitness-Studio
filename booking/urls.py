from django.urls import include, path

from rest_framework.routers import DefaultRouter

from booking.views import FitnessClassBookView

router = DefaultRouter()
router.register(r'', FitnessClassBookView, basename='fitness_class')


urlpatterns = [
    path('', include(router.urls)),
]