from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from booking_website.models import AuthUser
from django.utils.translation import gettext_lazy as _


@admin.register(AuthUser)
class AuthUserAdmin(UserAdmin):
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('first_name', 'last_name', 'email', 'password1', 'password2'),
            },
        ),
    )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', )}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
