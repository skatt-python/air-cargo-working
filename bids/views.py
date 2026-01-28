from django.shortcuts import render
from .models import Bid

def bid_list(request):
    bids = Bid.objects.all()
    return render(request, 'bids/bid_list.html', {'bids': bids})
