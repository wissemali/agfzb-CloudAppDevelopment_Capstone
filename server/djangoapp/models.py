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


class CarDealer(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    id = models.CharField(max_length=255, primary_key=True)
    lat = models.FloatField()
    long = models.FloatField()
    short_name = models.CharField(max_length=255)
    st = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)

  

class DealerReview(models.Model):
    dealership = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    purchase = models.BooleanField()
    review = models.TextField()
    purchase_date = models.DateField()
    car_make = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    car_year = models.PositiveIntegerField()
    sentiment = models.CharField(max_length=10)
    id = models.AutoField(primary_key=True)        


    def __str__(self):
        return "Dealer name: " + self.full_name



