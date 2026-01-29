from django.db import models
from django.contrib.auth.models import User
from shipments.models import Shipment


class Bid(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидает рассмотрения'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
        ('cancelled', 'Отменено агентом'),
    )

    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name='bids',
        verbose_name='Заявка'
    )
    agent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bids',
        verbose_name='Агент'
    )
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Предлагаемая цена'
    )
    proposed_departure_date = models.DateField(
        verbose_name='Предлагаемая дата отправления',
        null=True,
        blank=True
    )
    proposed_arrival_date = models.DateField(
        verbose_name='Предлагаемая дата прибытия',
        null=True,
        blank=True
    )
    notes = models.TextField(
        verbose_name='Комментарии и условия',
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Предложение #{self.id} к заявке #{self.shipment.id}"

    def is_pending(self):
        return self.status == 'pending'

    def can_be_accepted(self):
        return self.status == 'pending'

    def can_be_cancelled(self):
        return self.status == 'pending'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'