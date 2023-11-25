from django.conf import settings
from django.db import models


CustomUser = settings.AUTH_USER_MODEL

class BookingSummary (models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_location = models.CharField(max_length=300)
    destination = models.CharField(max_length=300)
    two_way = models.BooleanField()
    no_of_passengers = models.IntegerField()
    pickup_long = models.FloatField()
    pickup_lat = models.FloatField()
    dest_long = models.FloatField()
    dest_lat = models.FloatField()
    distance = models.FloatField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name
   

class Junction(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created', '-updated']



class PriceTable(models.Model):
    start_junction = models.ForeignKey(Junction, on_delete=models.CASCADE, related_name='start_junction_prices')
    end_junction = models.ForeignKey(Junction, on_delete=models.CASCADE, related_name='end_junction_prices')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Price from {self.start_junction} to {self.end_junction}'
    
    
    class Meta:
        ordering = ['-created', '-updated']



class Ride(models.Model):
    user = models.ForeignKey (CustomUser, on_delete=models.CASCADE)
    start_junction = models.ForeignKey(Junction, on_delete=models.SET_NULL, null=True, related_name='start_junction_rides')
    end_junction = models.ForeignKey(Junction, on_delete=models.SET_NULL, null=True, related_name='end_junction')
    no_of_passengers = models.IntegerField(default=1)
    two_way = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ride from {self.start_junction} to {self.end_junction}'


    class Meta:
        ordering = ['-created']


class Car(models.Model):
    driver = models.ForeignKey (CustomUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    license_plate = models.CharField(max_length=300)
    car_model = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return self.car_model
    

    class Meta:
        ordering = ['-created']

