from django.db import models
from django.contrib.auth.models import User
from shipments.models import Shipment


class Bid(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
        ('cancelled', 'Отменено'),
    ]

    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='bids')
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    proposed_departure_date = models.DateField()
    proposed_arrival_date = models.DateField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Предложение #{self.id} к заявке {self.shipment.title}"

    class Meta:
        ordering = ['-created_at']