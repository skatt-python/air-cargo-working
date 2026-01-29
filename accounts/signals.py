from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Создаем или обновляем профиль пользователя"""
    if created:
        # При создании пользователя создаем пустой профиль
        UserProfile.objects.create(user=instance)
    else:
        # При обновлении пользователя, убедимся что профиль существует
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            # На всякий случай, если профиль почему-то не создался
            UserProfile.objects.create(user=instance)