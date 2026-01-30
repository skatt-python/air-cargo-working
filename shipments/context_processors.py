"""
Контекстные процессоры для приложения shipments.
Добавляют дополнительные данные во все шаблоны.
"""
from .models import Notification


def notification_count(request):
    """
    Добавляет количество непрочитанных уведомлений в контекст всех шаблонов.
    Это позволяет отображать счетчик уведомлений в навигационной панели.
    """
    if request.user.is_authenticated:
        try:
            # Считаем только непрочитанные уведомления текущего пользователя
            count = Notification.objects.filter(user=request.user, is_read=False).count()
            return {'unread_notifications_count': count}
        except Exception:
            # Если что-то пошло не так (например, таблица еще не создана),
            # возвращаем 0
            return {'unread_notifications_count': 0}
    # Для неаутентифицированных пользователей счетчик всегда 0
    return {'unread_notifications_count': 0}