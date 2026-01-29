from django.urls import path
from . import views

app_name = 'shipments'

urlpatterns = [
    path('', views.shipment_list, name='shipment_list'),
    path('<int:shipment_id>/', views.shipment_detail, name='shipment_detail'),
]
