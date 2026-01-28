from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='shipment_list'), name='home'),
    path('shipments/', include('shipments.urls')),
    path('bids/', include('bids.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
