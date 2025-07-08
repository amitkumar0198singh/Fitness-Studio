from django.db import models

# Create your models here.


class FitnessClass(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    instructor = models.CharField(max_length=255, null=True, blank=True)
    max_slots = models.PositiveIntegerField(null=True, blank=True)
    available_slots = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    class_time = models.DateTimeField(null=True, blank=True)


    class Meta:
        verbose_name_plural = "Fitness Classes"
        ordering = ['class_time']
        db_table = 'fitness_class'

    def __str__(self):
        return f"{self.name} with {self.instructor} at {self.class_time}"
    


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, db_column='fitness_class')
    client_name = models.CharField(max_length=255, null=True, blank=True)
    client_email = models.CharField(max_length=255, null=True, blank=True)
    booking_time = models.DateTimeField(auto_now_add=True)
    booked_slots = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-booking_time']
        unique_together = ['fitness_class', 'client_email']
        db_table = 'booking'

    def __str__(self):
        return f"{self.client_name} has booked {self.fitness_class.name} at {self.booking_time}"