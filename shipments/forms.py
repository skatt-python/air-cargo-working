from django import forms
from .models import Shipment


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['title', 'description', 'cargo_type', 'weight', 'volume',
                  'origin_city', 'destination_city', 'departure_date',
                  'arrival_date', 'budget', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название заявки'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание груза, требования к перевозке'
            }),
            'cargo_type': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Введите вес в кг'
            }),
            'volume': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Введите объем в м³'
            }),
            'origin_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Город отправления'
            }),
            'destination_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Город назначения'
            }),
            'departure_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'arrival_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Предполагаемый бюджет'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        departure_date = cleaned_data.get('departure_date')
        arrival_date = cleaned_data.get('arrival_date')

        if departure_date and arrival_date and departure_date > arrival_date:
            self.add_error('arrival_date',
                           "Дата прибытия не может быть раньше даты отправления")

        return cleaned_data