from django import forms
from .models import Bid


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price', 'proposed_departure_date', 'proposed_arrival_date', 'notes']
        widgets = {
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите цену в рублях',
                'step': '0.01',
                'min': '0'
            }),
            'proposed_departure_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Выберите дату отправления'
            }),
            'proposed_arrival_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Выберите дату прибытия'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Дополнительные условия, комментарии...'
            }),
        }
        labels = {
            'price': 'Цена предложения (руб.)',
            'proposed_departure_date': 'Предлагаемая дата отправления',
            'proposed_arrival_date': 'Предлагаемая дата прибытия',
            'notes': 'Комментарии и условия'
        }
        help_texts = {
            'price': 'Укажите стоимость перевозки в рублях',
            'proposed_departure_date': 'Если не указано, будет использована дата из заявки',
            'proposed_arrival_date': 'Если не указано, будет использована дата из заявки',
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Цена должна быть больше нуля")
        return price

    def clean(self):
        cleaned_data = super().clean()
        departure_date = cleaned_data.get('proposed_departure_date')
        arrival_date = cleaned_data.get('proposed_arrival_date')

        if departure_date and arrival_date and departure_date > arrival_date:
            self.add_error('proposed_arrival_date',
                           "Дата прибытия не может быть раньше даты отправления")

        return cleaned_data