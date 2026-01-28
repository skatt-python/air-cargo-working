from django.shortcuts import render
from .models import Shipment

def shipment_list(request):
    shipments = Shipment.objects.all()
    return render(request, 'shipments/shipment_list.html', {'shipments': shipments})
