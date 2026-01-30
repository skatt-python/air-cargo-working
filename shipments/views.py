from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Shipment
from .forms import ShipmentForm  # Создадим позже


def shipment_list(request):
    """Список всех заявок"""
    shipments = Shipment.objects.filter(status='active').order_by('-created_at')

    # Агенты не видят свои собственные заявки
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        if request.user.profile.is_agent:
            shipments = shipments.exclude(owner=request.user)

    context = {
        'shipments': shipments,
        'title': 'Список заявок'
    }
    return render(request, 'shipments/shipment_list.html', context)


def shipment_detail(request, pk):
    """Детальная страница заявки"""
    shipment = get_object_or_404(Shipment, pk=pk)
    bids = shipment.bids.all().order_by('-created_at')

    context = {
        'shipment': shipment,
        'bids': bids,
        'title': shipment.title
    }
    return render(request, 'shipments/shipment_detail.html', context)


@login_required
def create_shipment(request):
    """Создание новой заявки"""
    if not request.user.profile.is_shipper:
        messages.error(request, "Только грузовладельцы могут создавать заявки.")
        return redirect('shipments:shipment_list')

    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            shipment = form.save(commit=False)
            shipment.owner = request.user
            shipment.status = 'active'
            shipment.save()
            messages.success(request, 'Заявка успешно создана!')
            # Используем reverse для получения URL
            return redirect('shipments:shipment_detail', pk=shipment.id)
        else:
            # Если форма невалидна, покажем ошибки
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
            print("Ошибки формы:", form.errors)  # Для отладки
    else:
        form = ShipmentForm()

    context = {
        'form': form,
        'title': 'Создать заявку'
    }
    return render(request, 'shipments/create_shipment.html', context)


@login_required
def my_shipments(request):
    """Мои заявки (для грузовладельца)"""
    if not request.user.profile.is_shipper:
        messages.error(request, "Только грузовладельцы могут просматривать свои заявки.")
        return redirect('dashboard')

    shipments = Shipment.objects.filter(owner=request.user).order_by('-created_at')

    context = {
        'shipments': shipments,
        'title': 'Мои заявки'
    }
    return render(request, 'shipments/my_shipments.html', context)