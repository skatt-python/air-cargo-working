# shipments/models.py - ОБНОВЛЕННАЯ ВЕРСИЯ С СОВМЕСТИМОСТЬЮ
from django.db import models
from django.conf import settings


class Shipment(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('active', 'Активна'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]

    # Существующие поля
    title = models.CharField('Название заявки', max_length=200)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shipments',
        verbose_name='Владелец'
    )
    description = models.TextField('Описание', blank=True)
    weight = models.DecimalField('Вес (кг)', max_digits=10, decimal_places=2)
    departure_city = models.CharField('Город отправления', max_length=100)
    arrival_city = models.CharField('Город назначения', max_length=100)
    estimated_price = models.DecimalField(
        'Ожидаемая стоимость',
        max_digits=12,
        decimal_places=2
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    # НОВЫЕ поля
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    cargo_type = models.CharField(
        'Тип груза',
        max_length=50,
        default='general',
        blank=True
    )
    accepted_bid = models.OneToOneField(
        'bids.Bid',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accepted_for_shipment',
        verbose_name='Принятое предложение'
    )

    class Meta:
        verbose_name = 'Заявка на перевозку'
        verbose_name_plural = 'Заявки на перевозку'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} (#{self.id})'

    def has_accepted_bid(self):
        """Есть ли принятое предложение"""
        return self.accepted_bid is not None