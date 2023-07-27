from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Any other fields you want to include in the CarMake model

    def __str__(self):
        return self.name


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.CharField(max_length=100)
    TYPE_CHOICES = (
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        # Add more choices as needed
    )
    car_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    year = models.DateField()
    # Any other fields you want to include in the CarModel model

    def __str__(self):
        return f"{self.car_make.name} - {self.name} ({self.car_type})"

