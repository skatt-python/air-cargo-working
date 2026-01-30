#!/usr/bin/env python
import os
import django
import sys

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile


def clean_profiles():
    """Очищает дублирующиеся профили и создает недостающие"""
    print("=" * 50)
    print("🧹 ОЧИСТКА БАЗЫ ДАННЫХ ОТ ДУБЛИРУЮЩИХСЯ ПРОФИЛЕЙ")
    print("=" * 50)

    # Удаляем ВСЕ профили
    print("\n1. Удаление всех старых профилей...")
    count, _ = UserProfile.objects.all().delete()
    print(f"   ✅ Удалено {count} профилей")

    # Создаем новые профили для всех пользователей
    print("\n2. Создание новых профилей...")
    users = User.objects.all()
    created = 0

    for user in users:
        # Создаем профиль с дефолтными значениями
        UserProfile.objects.create(
            user=user,
            role='shipper',  # значение по умолчанию
            company_name='',
            phone_number=''
        )
        created += 1
        print(f"   ✅ Создан профиль для {user.username}")

    print(f"\n3. Итого создано {created} профилей")

    # Проверяем целостность
    print("\n4. Проверка целостности данных...")
    users_count = User.objects.count()
    profiles_count = UserProfile.objects.count()

    if users_count == profiles_count:
        print(f"   ✅ Все хорошо! Пользователей: {users_count}, Профилей: {profiles_count}")
    else:
        print(f"   ⚠️ Несоответствие! Пользователей: {users_count}, Профилей: {profiles_count}")

    print("\n" + "=" * 50)
    print("✅ ОЧИСТКА ЗАВЕРШЕНА!")
    print("=" * 50)


if __name__ == '__main__':
    # Подтверждение действия
    response = input("\n⚠️  Вы уверены что хотите удалить ВСЕ профили и создать заново? (yes/no): ")

    if response.lower() == 'yes':
        clean_profiles()
    else:
        print("❌ Операция отменена")
        sys.exit(0)