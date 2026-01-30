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

class Notification(models.Model):
    """Модель уведомлений для пользователей"""
    NOTIFICATION_TYPES = (
        ('bid_created', 'Новое предложение'),
        ('bid_accepted', 'Предложение принято'),
        ('bid_rejected', 'Предложение отклонено'),
        ('bid_cancelled', 'Предложение отменено'),
        ('shipment_created', 'Новая заявка'),
        ('shipment_updated', 'Заявка обновлена'),
        ('shipment_status', 'Изменение статуса заявки'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.user.username}"

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


class Notification(models.Model):
    """Модель уведомлений для пользователей"""
    NOTIFICATION_TYPES = (
        ('bid_created', 'Новое предложение'),
        ('bid_accepted', 'Предложение принято'),
        ('bid_rejected', 'Предложение отклонено'),
        ('bid_cancelled', 'Предложение отменено'),
        ('shipment_created', 'Новая заявка'),
        ('shipment_updated', 'Заявка обновлена'),
        ('shipment_status', 'Изменение статуса заявки'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.user.username}"