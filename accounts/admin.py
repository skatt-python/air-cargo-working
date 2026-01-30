from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')

    def get_role(self, obj):
        return obj.profile.get_role_display() if hasattr(obj, 'profile') else 'Нет профиля'

    get_role.short_description = 'Роль'


# Удаляем старую регистрацию и регистрируем заново
admin.site.unregister(User)
admin.site.register(User, UserAdmin)