from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Shipment(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('active', 'Активная'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    )

    CARGO_TYPE_CHOICES = (
        ('general', 'Генеральный груз'),
        ('perishable', 'Скоропортящийся'),
        ('dangerous', 'Опасный груз'),
        ('live_animals', 'Живые животные'),
        ('valuables', 'Ценности'),
        ('other', 'Другое'),
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shipments',
        verbose_name='Владелец'
    )
    title = models.CharField(max_length=200, verbose_name='Название заявки')
    description = models.TextField(verbose_name='Описание груза')
    cargo_type = models.CharField(
        max_length=20,
        choices=CARGO_TYPE_CHOICES,
        default='general',
        verbose_name='Тип груза'
    )
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Вес (кг)'
    )
    volume = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Объем (м³)',
        null=True,
        blank=True
    )
    origin_city = models.CharField(max_length=100, verbose_name='Город отправления')
    destination_city = models.CharField(max_length=100, verbose_name='Город назначения')
    departure_date = models.DateField(verbose_name='Дата отправления')
    arrival_date = models.DateField(verbose_name='Дата прибытия')
    budget = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Бюджет',
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def is_active(self):
        return self.status == 'active'

    def can_be_bidded(self):
        return self.status == 'active' and self.departure_date > timezone.now().date()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'