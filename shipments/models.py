from django.db import models
from django.contrib.auth.models import User


class Shipment(models.Model):
    STATUS_CHOICES = [
        ('open', 'Открыта'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]

    CARGO_TYPE_CHOICES = [
        ('general', 'Генеральный груз'),
        ('perishable', 'Скоропортящийся'),
        ('dangerous', 'Опасный груз'),
        ('fragile', 'Хрупкий'),
        ('oversized', 'Крупногабаритный'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    cargo_type = models.CharField(max_length=50, choices=CARGO_TYPE_CHOICES)
    weight = models.DecimalField(max_digits=10, decimal_places=2, help_text="В кг")
    volume = models.DecimalField(max_digits=10, decimal_places=2, help_text="В м³")
    origin_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    departure_date = models.DateField()
    arrival_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']