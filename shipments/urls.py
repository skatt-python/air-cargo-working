from django.urls import path
from . import views

app_name = 'shipments'

urlpatterns = [
    path('', views.shipment_list, name='shipment_list'),
    path('create/', views.create_shipment, name='create_shipment'),
    path('my/', views.my_shipments, name='my_shipments'),
    path('<int:pk>/', views.shipment_detail, name='shipment_detail'),
path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
]