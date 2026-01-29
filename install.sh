#!/bin/bash

echo ""
echo "========================================================"
echo "🚀 Установка системы аутентификации AirCargo"
echo "========================================================"
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден! Установите Python3 и повторите."
    exit 1
fi

echo "✅ Python3 обнаружен: $(python3 --version)"

# Проверка pip
if ! command -v pip3 &> /dev/null; then
    echo "📦 Установка pip3..."
    python3 -m ensurepip --upgrade
fi

echo "✅ pip обнаружен: $(pip3 --version)"

# Активация/создание виртуального окружения
if [ -d ".venv" ]; then
    echo "✅ Виртуальное окружение найдено"
    source .venv/bin/activate
    echo "🔧 Активировано виртуальное окружение"
else
    echo "📦 Создание виртуального окружения..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "✅ Виртуальное окружение создано и активировано"
fi

# Обновление pip
echo ""
echo "📦 Обновление pip..."
pip install --upgrade pip

# Установка зависимостей
echo ""
echo "📦 Установка зависимостей из requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Зависимости установлены"
else
    echo "⚠️ Файл requirements.txt не найден"
    echo "📦 Установка базовых зависимостей..."
    pip install django==4.1.13
    echo "✅ Django установлен"
fi

# Создание необходимых директорий
echo ""
echo "📁 Создание необходимых директорий..."
mkdir -p static/css static/js static/images media/uploads

# Создание миграций
echo ""
echo "🗄 Создание миграций для приложений..."
python manage.py makemigrations accounts
python manage.py makemigrations shipments
python manage.py makemigrations bids

# Применение миграций
echo ""
echo "🗄 Применение миграций к базе данных..."
python manage.py migrate

# Создание суперпользователя (опционально)
echo ""
echo "👑 Хотите создать суперпользователя? (y/n)"
read -r create_superuser

if [[ "$create_superuser" =~ ^[Yy]$ ]]; then
    echo "Создание суперпользователя..."
    python manage.py createsuperuser
    echo "✅ Суперпользователь создан"
else
    echo "⚠️ Суперпользователь не создан"
    echo "   Вы можете создать его позже командой:"
    echo "   python manage.py createsuperuser"
fi

# Сбор статических файлов
echo ""
echo "🎨 Сбор статических файлов..."
python manage.py collectstatic --noinput
echo "✅ Статические файлы собраны"

# Создание тестовых пользователей (опционально)
echo ""
echo "👥 Хотите создать тестовых пользователей? (y/n)"
read -r create_test_users

if [[ "$create_test_users" =~ ^[Yy]$ ]]; then
    echo "Создание тестовых пользователей..."
    python manage.py shell << EOF
from django.contrib.auth.models import User
from accounts.models import UserProfile

# Создание тестового грузовладельца
if not User.objects.filter(username='shipper_test').exists():
    shipper = User.objects.create_user(
        username='shipper_test',
        email='shipper@test.com',
        password='test123456'
    )
    shipper_profile = shipper.profile
    shipper_profile.role = 'shipper'
    shipper_profile.company_name = 'Тестовая компания грузовладельца'
    shipper_profile.phone_number = '+7 (999) 111-22-33'
    shipper_profile.save()
    print('✅ Создан грузовладелец: shipper_test / test123456')

# Создание тестового агента
if not User.objects.filter(username='agent_test').exists():
    agent = User.objects.create_user(
        username='agent_test',
        email='agent@test.com',
        password='test123456'
    )
    agent_profile = agent.profile
    agent_profile.role = 'agent'
    agent_profile.company_name = 'Тестовая транспортная компания'
    agent_profile.phone_number = '+7 (999) 444-55-66'
    agent_profile.save()
    print('✅ Создан агент: agent_test / test123456')
EOF
fi

echo ""
echo "========================================================"
echo "✅ УСТАНОВКА ЗАВЕРШЕНА!"
echo "========================================================"
echo ""
echo "📋 КОМАНДЫ ДЛЯ ЗАПУСКА:"
echo ""
echo "1. 🔧 Активировать виртуальное окружение:"
echo "   source .venv/bin/activate"
echo ""
echo "2. 🚀 Запустить сервер разработки:"
echo "   python manage.py runserver 8001"
echo ""
echo "3. 🌐 Открыть в браузере:"
echo "   - Главная: http://localhost:8001/"
echo "   - Регистрация: http://localhost:8001/accounts/register/"
echo "   - Вход: http://localhost:8001/accounts/login/"
echo "   - Админка: http://localhost:8001/admin/"
echo ""
echo "4. 👥 Тестовые пользователи (если созданы):"
echo "   - Грузовладелец: shipper_test / test123456"
echo "   - Агент: agent_test / test123456"
echo ""
echo "========================================================"
echo "🛠 Для остановки сервера нажмите Ctrl+C в терминале"
echo "========================================================"