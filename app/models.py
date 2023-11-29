from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=80)
    url = models.URLField(unique=True)
    description = models.TextField(default="",blank=True)
    price = models.FloatField()
    color = models.CharField(max_length=80)
    years = models.IntegerField()
    motors = models.CharField(max_length=80)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f"{self.id} {self.name}"
    
    def __str__(self):
        return self.full_name()
    

class Rent_car(models.Model):
    car = models.OneToOneField(to=Car,on_delete=models.CASCADE)

    rent_number = models.CharField(max_length=10)
    car_number = models.CharField(max_length=8)
    car_yoqilgi = models.CharField(max_length=45)
    model = models.CharField(max_length=80)

    def __str__(self) -> str:
        return f"{self.car.full_name()} {self.car_yoqilgi}"
    