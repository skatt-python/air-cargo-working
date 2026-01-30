from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import transaction
from django.apps import apps


@receiver(post_save)
def handle_post_save(sender, instance, created, **kwargs):
    """
    Универсальный обработчик для создания уведомлений
    """
    # Получаем модель Notification динамически, чтобы избежать циклического импорта
    Notification = apps.get_model('shipments', 'Notification')

    # Обработка создания/обновления Bid
    if sender.__name__ == 'Bid':
        if created:
            # Создание нового предложения - уведомление владельцу
            try:
                Notification.objects.create(
                    user=instance.shipment.owner,
                    message=f'Новое предложение к вашей заявке "{instance.shipment.title}". Цена: {instance.price} руб.',
                    notification_type='bid_created',
                    link=reverse('bid_detail', args=[instance.id])
                )
                print(f"Создано уведомление о новом предложении для пользователя {instance.shipment.owner.username}")
            except Exception as e:
                print(f"Ошибка создания уведомления о предложении: {e}")
        else:
            # Изменение статуса существующего предложения
            try:
                # Получаем предыдущее значение статуса из базы данных
                old_instance = sender.objects.get(id=instance.id)

                if old_instance.status != instance.status:
                    if instance.status == 'accepted':
                        # Уведомление агенту
                        Notification.objects.create(
                            user=instance.agent,
                            message=f'Ваше предложение к заявке "{instance.shipment.title}" принято!',
                            notification_type='bid_accepted',
                            link=reverse('bid_detail', args=[instance.id])
                        )
                        print(f"Создано уведомление о принятии предложения для агента {instance.agent.username}")

                    elif instance.status == 'rejected':
                        # Уведомление агенту
                        Notification.objects.create(
                            user=instance.agent,
                            message=f'Ваше предложение к заявке "{instance.shipment.title}" отклонено.',
                            notification_type='bid_rejected',
                            link=reverse('bid_detail', args=[instance.id])
                        )
                        print(f"Создано уведомление об отклонении предложения для агента {instance.agent.username}")

                    elif instance.status == 'cancelled':
                        # Уведомление владельцу
                        Notification.objects.create(
                            user=instance.shipment.owner,
                            message=f'Предложение от {instance.agent.username} отменено.',
                            notification_type='bid_cancelled',
                            link=reverse('shipment_detail', args=[instance.shipment.id])
                        )
                        print(
                            f"Создано уведомление об отмене предложения для владельца {instance.shipment.owner.username}")
            except Exception as e:
                print(f"Ошибка обновления уведомления о предложении: {e}")

    # Обработка создания Shipment
    elif sender.__name__ == 'Shipment':
        if created:
            # Новая заявка - уведомляем всех агентов
            try:
                agents = User.objects.filter(userprofile__role='agent')
                for agent in agents:
                    Notification.objects.create(
                        user=agent,
                        message=f'Новая заявка "{instance.title}" в городе {instance.origin_city}.',
                        notification_type='shipment_created',
                        link=reverse('shipment_detail', args=[instance.id])
                    )
                print(f"Созданы уведомления о новой заявке для {agents.count()} агентов")
            except Exception as e:
                print(f"Ошибка создания уведомлений о новой заявке: {e}")
        else:
            # Изменение существующей заявки
            try:
                # Проверяем изменение статуса
                old_instance = sender.objects.get(id=instance.id)

                if old_instance.status != instance.status:
                    # Уведомление владельцу
                    Notification.objects.create(
                        user=instance.owner,
                        message=f'Статус вашей заявки "{instance.title}" изменен на: {instance.get_status_display()}',
                        notification_type='shipment_status',
                        link=reverse('shipment_detail', args=[instance.id])
                    )
                    print(f"Создано уведомление об изменении статуса для владельца {instance.owner.username}")

                    # Уведомление всем агентам с предложениями
                    # Используем try-except на случай, если связь bids еще не существует
                    try:
                        for bid in instance.bids.all():
                            Notification.objects.create(
                                user=bid.agent,
                                message=f'Статус заявки "{instance.title}" изменен на: {instance.get_status_display()}',
                                notification_type='shipment_status',
                                link=reverse('shipment_detail', args=[instance.id])
                            )
                        print(f"Созданы уведомления об изменении статуса для {instance.bids.count()} агентов")
                    except Exception as e:
                        print(f"Ошибка создания уведомлений для агентов: {e}")
            except Exception as e:
                print(f"Ошибка обновления уведомлений о заявке: {e}")


@receiver(post_save, sender=User)
def create_user_notifications(sender, instance, created, **kwargs):
    """
    Создание тестового уведомления при регистрации пользователя
    """
    if created:
        try:
            Notification = apps.get_model('shipments', 'Notification')
            Notification.objects.create(
                user=instance,
                message='Добро пожаловать в Air Cargo System!',
                notification_type='shipment_created',
                is_read=False
            )
            print(f"Создано приветственное уведомление для {instance.username}")
        except Exception as e:
            print(f"Ошибка создания приветственного уведомления: {e}")