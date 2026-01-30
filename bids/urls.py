from django.urls import path
from . import views

app_name = 'bids'

urlpatterns = [
    path('', views.bid_list, name='bid_list'),
    path('create/<int:shipment_id>/', views.create_bid, name='create_bid'),
    path('<int:bid_id>/', views.bid_detail, name='bid_detail'),
    path('<int:bid_id>/accept/', views.accept_bid, name='accept_bid'),
    path('<int:bid_id>/reject/', views.reject_bid, name='reject_bid'),
    path('<int:bid_id>/cancel/', views.cancel_bid, name='cancel_bid'),
]