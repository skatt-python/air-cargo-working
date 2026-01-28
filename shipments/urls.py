from django.urls import path
from . import views

urlpatterns = [
    path('', views.shipment_list, name='shipment_list'),
]
