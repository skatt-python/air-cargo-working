from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Создаем или обновляем профиль пользователя"""
    if created:
        # При создании пользователя создаем профиль с дефолтными значениями
        UserProfile.objects.get_or_create(
            user=instance,
            defaults={
                'role': 'shipper',  # значение по умолчанию
                'company_name': '',
                'phone_number': ''
            }
        )
    else:
        # При обновлении пользователя, убедимся что профиль существует
        UserProfile.objects.get_or_create(user=instance)