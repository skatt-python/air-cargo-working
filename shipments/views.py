from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Shipment
from bids.models import Bid


def shipment_list(request):
    shipments = Shipment.objects.filter(status='active').order_by('-created_at')
    return render(request, 'shipments/shipment_list.html', {'shipments': shipments})


@login_required
def shipment_detail(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    
    # Проверяем, есть ли у пользователя активное предложение к этой заявке
    user_has_pending_bid = False
    if request.user.is_authenticated and request.user != shipment.owner:
        user_has_pending_bid = Bid.objects.filter(
            shipment=shipment,
            carrier_agent=request.user,
            status='pending'
        ).exists()
    
    return render(request, 'shipments/shipment_detail.html', {
        'shipment': shipment,
        'user_has_pending_bid': user_has_pending_bid,
    })
