from django import forms
from .models import Bid


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price', 'currency', 'notes']
        widgets = {
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Введите цену'
            }),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Дополнительная информация о вашем предложении...'
            }),
        }
        labels = {
            'price': 'Цена предложения',
            'currency': 'Валюта',
            'notes': 'Дополнительные заметки',
        }
