from django.db import models
from django.conf import settings
from shipments.models import Shipment

class Bid(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    carrier_agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Bid #{self.id} for Shipment #{self.shipment.id}"
