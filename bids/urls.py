from django.urls import path
from . import views

urlpatterns = [
    path('', views.bid_list, name='bid_list'),
]
