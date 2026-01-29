# bids/models.py - ОБНОВЛЕННАЯ ВЕРСИЯ С СОВМЕСТИМОСТЬЮ
from django.db import models
from django.conf import settings
from shipments.models import Shipment


class Bid(models.Model):
    BID_STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
        ('cancelled', 'Отменено'),
    ]

    # Существующие поля (уже есть в базе)
    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name='bids'  # Добавим related_name для удобства
    )
    carrier_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submitted_bids'
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # НОВЫЕ поля (добавим через миграцию)
    status = models.CharField(
        max_length=20,
        choices=BID_STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    currency = models.CharField(
        max_length=3,
        default='USD',
        choices=[('USD', 'USD'), ('EUR', 'EUR'), ('RUB', 'RUB')],
        verbose_name='Валюта'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'
        ordering = ['-created_at']

    def __str__(self):
        return f'Предложение #{self.id} для заявки #{self.shipment.id}'

    def accept(self):
        """Принять предложение"""
        self.status = 'accepted'
        self.save()

    def reject(self):
        """Отклонить предложение"""
        self.status = 'rejected'
        self.save()