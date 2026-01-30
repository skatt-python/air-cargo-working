from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bid, Shipment
from .forms import BidForm


@login_required
def create_bid(request, shipment_id):
    """Создание предложения к заявке"""
    shipment = get_object_or_404(Shipment, id=shipment_id)

    # Проверка: только агенты могут создавать предложения
    if not request.user.profile.is_agent:
        messages.error(request, "Только агенты могут создавать предложения.")
        return redirect('shipments:shipment_detail', pk=shipment_id)

    # Проверка: агент не может делать предложения на свои заявки
    if shipment.owner == request.user:
        messages.error(request, "Вы не можете делать предложения на свои заявки.")
        return redirect('shipments:shipment_detail', pk=shipment_id)

    # Проверка: только активные заявки
    if shipment.status != 'active':
        messages.error(request, "Нельзя делать предложения к неактивным заявкам.")
        return redirect('shipments:shipment_detail', pk=shipment_id)

    # Проверка: не более одного активного предложения на заявку
    existing_bid = Bid.objects.filter(
        shipment=shipment,
        agent=request.user,
        status='pending'
    ).first()

    if existing_bid:
        messages.warning(request, f"У вас уже есть активное предложение к этой заявке (#{existing_bid.id}).")
        return redirect('bids:bid_detail', bid_id=existing_bid.id)

    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.shipment = shipment
            bid.agent = request.user
            bid.save()
            messages.success(request, 'Предложение успешно создано!')
            return redirect('bids:bid_detail', bid_id=bid.id)
    else:
        form = BidForm()

    context = {
        'form': form,
        'shipment': shipment,
        'title': 'Создать предложение'
    }
    return render(request, 'bids/create_bid.html', context)


def bid_list(request):
    """Список всех предложений"""
    bids = Bid.objects.all().order_by('-created_at')

    # Если пользователь авторизован, показываем его предложения первыми
    if request.user.is_authenticated:
        context = {
            'bids': bids,
            'user_bids': request.user.bids.all().order_by('-created_at'),
            'title': 'Все предложения'
        }
    else:
        context = {
            'bids': bids,
            'title': 'Все предложения'
        }

    return render(request, 'bids/bid_list.html', context)


def bid_detail(request, bid_id):
    """Детальная страница предложения"""
    bid = get_object_or_404(Bid, id=bid_id)

    context = {
        'bid': bid,
        'title': f'Предложение #{bid.id}'
    }
    return render(request, 'bids/bid_detail.html', context)


@login_required
def accept_bid(request, bid_id):
    """Принятие предложения владельцем заявки"""
    bid = get_object_or_404(Bid, id=bid_id)

    # Проверка прав: только владелец заявки может принимать предложения
    if bid.shipment.owner != request.user:
        messages.error(request, "Вы не можете принимать это предложение.")
        return redirect('bids:bid_detail', bid_id=bid_id)

    # Проверка: только pending предложения можно принять
    if bid.status != 'pending':
        messages.error(request, "Это предложение уже обработано.")
        return redirect('bids:bid_detail', bid_id=bid_id)

    # Проверка: заявка должна быть активной
    if bid.shipment.status != 'active':
        messages.error(request, "Нельзя принимать предложения к неактивным заявкам.")
        return redirect('bids:bid_detail', bid_id=bid_id)

    # Принимаем предложение
    bid.status = 'accepted'
    bid.save()

    # Отклоняем все остальные предложения к этой заявке
    Bid.objects.filter(
        shipment=bid.shipment,
        status='pending'
    ).exclude(id=bid_id).update(status='rejected')

    # Меняем статус заявки
    bid.shipment.status = 'in_progress'
    bid.shipment.save()

    messages.success(request, 'Предложение принято! Остальные предложения отклонены.')
    return redirect('bids:bid_detail', bid_id=bid_id)


@login_required
def reject_bid(request, bid_id):
    """Отклонение предложения владельцем заявки"""
    bid = get_object_or_404(Bid, id=bid_id)

    # Проверка прав: только владелец заявки может отклонять предложения
    if bid.shipment.owner != request.user:
        messages.error(request, "Вы не можете отклонять это предложение.")
        return redirect('bids:bid_detail', bid_id=bid_id)

    # Проверка: только pending предложения можно отклонить
    if bid.status != 'pending':
        messages.error(request, "Это предложение уже обработано.")
        return redirect('bids:bid_detail', bid_id=bid_id)

    bid.status = 'rejected'
    bid.save()
    messages.success(request, 'Предложение отклонено.')
    return redirect('bids:bid_detail', bid_id=bid_id)


@login_required
def cancel_bid(request, bid_id):
    """Отмена предложения агентом"""
    bid = get_object_or_404(Bid, id=bid_id)

    # Проверка прав: только агент может отменять свои предложения
    if bid.agent != request.user:
        messages.error(request, "Вы не можете отменять это предложение.")
        return redirect('bids:bid_detail', bid_id=bid_id)

    # Проверка: только pending предложения можно отменить
    if bid.status != 'pending':
        messages.error(request, "Нельзя отменить уже обработанное предложение.")
        return redirect('bids:bid_detail', bid_id=bid_id)

    bid.status = 'cancelled'
    bid.save()
    messages.success(request, 'Предложение отменено.')
    return redirect('bids:bid_list')