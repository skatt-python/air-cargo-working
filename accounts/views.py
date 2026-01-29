from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import UserProfile


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Регистрация успешна! Добро пожаловать, {user.username}!')

            if user.profile.is_shipper:
                return redirect('dashboard')
            else:
                return redirect('dashboard')

        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
        'title': 'Регистрация'
    }
    return render(request, 'accounts/register.html', context)


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        messages.success(self.request, f'Добро пожаловать, {form.get_user().username}!')
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('dashboard')  # Всегда перенаправлять на dashboard

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)


@login_required
def profile(request):
    user = request.user
    profile = user.profile

    context = {
        'user': user,
        'profile': profile,
        'title': 'Мой профиль'
    }
    return render(request, 'accounts/profile.html', context)