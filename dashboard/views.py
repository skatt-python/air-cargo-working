from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shipments.models import Shipment
from bids.models import Bid


@login_required
def dashboard(request):
    user = request.user

    if user.profile.is_shipper:
        # Для грузовладельца
        shipments = user.shipments.all()
        active_shipments = shipments.filter(status='active')[:5]
        recent_bids = Bid.objects.filter(shipment__owner=user).order_by('-created_at')[:5]

        context = {
            'user': user,
            'shipments': shipments,
            'active_shipments': active_shipments,
            'recent_bids': recent_bids,
            'is_shipper': True
        }
    else:
        # Для агента
        bids = user.bids.all()
        pending_bids = bids.filter(status='pending')
        active_shipments = Shipment.objects.filter(status='active').exclude(owner=user)[:5]

        context = {
            'user': user,
            'bids': bids,
            'pending_bids': pending_bids,
            'active_shipments': active_shipments,
            'is_shipper': False
        }

    return render(request, 'dashboard/dashboard.html', context)


def home(request):
    """Главная страница для неавторизованных пользователей"""
    if request.user.is_authenticated:
        return dashboard(request)
    return render(request, 'dashboard/home.html')