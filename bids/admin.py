from django.contrib import admin
from .models import Bid

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'shipment', 'agent', 'price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('shipment__title', 'agent__username', 'notes')
    list_select_related = ('shipment', 'agent')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('shipment', 'agent', 'status')
        }),
        ('Детали предложения', {
            'fields': ('price', 'proposed_departure_date', 'proposed_arrival_date', 'notes')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )