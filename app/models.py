from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null= True)

    def __str__(self) -> str:
        return self.name

class Car(models.Model):
    name = models.CharField(max_length=80)
    url = models.URLField(unique=True)
    description = models.TextField(default="",blank=True)
    price = models.FloatField()
    color = models.CharField(max_length=80)
    years = models.IntegerField()
    motors = models.CharField(max_length=80)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f"{self.id} {self.name}"
    
    def __str__(self):
        return self.full_name()
    

    