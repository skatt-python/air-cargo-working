from django.db import models
from django.conf import settings

class Shipment(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    estimated_price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
