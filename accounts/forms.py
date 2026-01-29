from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'})
    )

    ROLE_CHOICES = (
        ('shipper', 'Грузовладелец'),
        ('agent', 'Агент перевозчика'),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label='Регистрация как',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    company_name = forms.CharField(
        max_length=100,
        required=False,
        label='Название компании',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Необязательно'})
    )

    phone_number = forms.CharField(
        max_length=20,
        required=False,
        label='Телефон',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (XXX) XXX-XX-XX'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role', 'company_name', 'phone_number')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Подтвердите пароль'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            # Не создаем профиль заново, а обновляем существующий (созданный сигналом)
            user.profile.role = self.cleaned_data['role']
            user.profile.company_name = self.cleaned_data.get('company_name', '')
            user.profile.phone_number = self.cleaned_data.get('phone_number', '')
            user.profile.save()

        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )