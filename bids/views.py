from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Bid
from shipments.models import Shipment
from .forms import BidForm


@login_required
def create_bid(request, shipment_id):
    """Создание предложения к заявке"""
    shipment = get_object_or_404(Shipment, id=shipment_id)
    
    # Проверяем, что пользователь не владелец заявки
    if request.user == shipment.owner:
        messages.error(request, 'Вы не можете создавать предложения к своим заявкам.')
        return redirect('shipments:shipment_detail', shipment_id=shipment_id)
    
    # Проверяем, что заявка активна
    if shipment.status != 'active':
        messages.error(request, 'Нельзя создавать предложения к неактивной заявке.')
        return redirect('shipments:shipment_detail', shipment_id=shipment_id)
    
    # Проверяем, нет ли уже предложения от этого пользователя
    existing_bid = Bid.objects.filter(
        shipment=shipment,
        carrier_agent=request.user,
        status='pending'
    ).first()
    
    if existing_bid:
        messages.warning(request, 'У вас уже есть активное предложение для этой заявки.')
        return redirect('shipments:shipment_detail', shipment_id=shipment_id)
    
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.shipment = shipment
            bid.carrier_agent = request.user
            bid.save()
            
            messages.success(request, 'Предложение успешно создано!')
            return redirect('shipments:shipment_detail', shipment_id=shipment_id)
    else:
        form = BidForm(initial={
            'price': shipment.estimated_price,
            'currency': 'USD',
        })
    
    return render(request, 'bids/create_bid.html', {
        'form': form,
        'shipment': shipment,
    })


@login_required
def bid_list(request):
    """Список всех предложений пользователя"""
    user_bids = Bid.objects.filter(carrier_agent=request.user).order_by('-created_at')
    
    return render(request, 'bids/bid_list.html', {
        'bids': user_bids,
    })


@login_required
def bid_detail(request, bid_id):
    """Детальная страница предложения"""
    bid = get_object_or_404(Bid, id=bid_id)
    
    # Проверяем права доступа
    if request.user not in [bid.carrier_agent, bid.shipment.owner]:
        messages.error(request, 'У вас нет прав для просмотра этого предложения.')
        return redirect('dashboard:dashboard')
    
    # ИСПРАВЛЕНО: Убираем проверку shipment.status == 'active' для can_accept
    # Владелец может принять предложение если заявка активна ИЛИ уже в работе
    can_accept = (request.user == bid.shipment.owner and 
                  bid.status == 'pending' and 
                  bid.shipment.status in ['active', 'in_progress'])
    can_reject = (request.user == bid.shipment.owner and bid.status == 'pending')
    can_cancel = (request.user == bid.carrier_agent and bid.status == 'pending')
    
    return render(request, 'bids/bid_detail.html', {
        'bid': bid,
        'can_accept': can_accept,
        'can_reject': can_reject,
        'can_cancel': can_cancel,
    })


@login_required
@require_POST
def accept_bid(request, bid_id):
    """Принять предложение"""
    bid = get_object_or_404(Bid, id=bid_id)
    
    # Проверяем права
    if request.user != bid.shipment.owner:
        messages.error(request, 'Только владелец заявки может принимать предложения.')
        return redirect('dashboard:dashboard')
    
    if bid.status != 'pending':
        messages.error(request, 'Это предложение уже обработано.')
        return redirect('bids:bid_detail', bid_id=bid_id)
    
    # Проверяем, что заявка еще активна или в работе
    if bid.shipment.status not in ['active', 'in_progress']:
        messages.error(request, 'Нельзя принять предложение к неактивной заявке.')
        return redirect('bids:bid_detail', bid_id=bid_id)
    
    # Проверяем, нет ли уже принятого предложения
    if bid.shipment.has_accepted_bid():
        messages.error(request, 'У этой заявки уже есть принятое предложение.')
        return redirect('bids:bid_detail', bid_id=bid_id)
    
    # Принимаем предложение
    bid.accept()
    
    # Обновляем заявку
    shipment = bid.shipment
    shipment.accepted_bid = bid
    shipment.status = 'in_progress'
    shipment.save()
    
    # Отклоняем все остальные предложения к этой заявке
    Bid.objects.filter(
        shipment=shipment,
        status='pending'
    ).exclude(id=bid.id).update(status='rejected')
    
    messages.success(request, 'Предложение принято! Заявка переведена в статус "В работе".')
    return redirect('shipments:shipment_detail', shipment_id=shipment.id)


@login_required
@require_POST
def reject_bid(request, bid_id):
    """Отклонить предложение"""
    bid = get_object_or_404(Bid, id=bid_id)
    
    if request.user != bid.shipment.owner:
        messages.error(request, 'Только владелец заявки может отклонять предложения.')
        return redirect('dashboard:dashboard')
    
    if bid.status != 'pending':
        messages.error(request, 'Это предложение уже обработано.')
        return redirect('bids:bid_detail', bid_id=bid_id)
    
    bid.reject()
    messages.success(request, 'Предложение отклонено.')
    return redirect('shipments:shipment_detail', shipment_id=bid.shipment.id)


@login_required
@require_POST
def cancel_bid(request, bid_id):
    """Отменить предложение (агент)"""
    bid = get_object_or_404(Bid, id=bid_id)
    
    if request.user != bid.carrier_agent:
        messages.error(request, 'Только создатель предложения может его отменить.')
        return redirect('dashboard:dashboard')
    
    if bid.status != 'pending':
        messages.error(request, 'Нельзя отменить обработанное предложение.')
        return redirect('bids:bid_detail', bid_id=bid_id)
    
    bid.status = 'cancelled'
    bid.save()
    
    messages.success(request, 'Предложение отменено.')
    return redirect('bids:bid_list')
