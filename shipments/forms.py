from django import forms
from .models import Shipment


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['title', 'description', 'cargo_type', 'weight', 'volume',
                  'origin_city', 'destination_city', 'departure_date',
                  'arrival_date', 'budget']
        # УБРАЛИ 'status' - он будет устанавливаться автоматически

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название заявки',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание груза, требования к перевозке',
                'required': True
            }),
            'cargo_type': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': 'Введите вес в кг',
                'required': True
            }),
            'volume': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Введите объем в м³'
            }),
            'origin_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Город отправления',
                'required': True
            }),
            'destination_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Город назначения',
                'required': True
            }),
            'departure_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'arrival_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Предполагаемый бюджет'
            }),
        }

        labels = {
            'title': 'Название заявки*',
            'description': 'Описание груза*',
            'cargo_type': 'Тип груза*',
            'weight': 'Вес (кг)*',
            'volume': 'Объем (м³)',
            'origin_city': 'Город отправления*',
            'destination_city': 'Город назначения*',
            'departure_date': 'Дата отправления*',
            'arrival_date': 'Дата прибытия*',
            'budget': 'Бюджет (руб.)',
        }

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight <= 0:
            raise forms.ValidationError("Вес должен быть больше 0")
        return weight

    def clean(self):
        cleaned_data = super().clean()
        departure_date = cleaned_data.get('departure_date')
        arrival_date = cleaned_data.get('arrival_date')

        if departure_date and arrival_date and departure_date > arrival_date:
            self.add_error('arrival_date',
                           "Дата прибытия не может быть раньше даты отправления")

        return cleaned_data