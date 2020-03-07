from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User, Token


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_superuser', 'is_staff', 'is_delete')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display = ["id", "email", "first_name", "last_name", "is_superuser", "is_active", "is_delete"]

    list_filter = ('email', 'is_delete')

    ordering = ('-id',)

    search_fields = ('first_name', 'last_name', 'email')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(User, UserAdmin)
# hide original token model in admin panel
admin.site.register(Token)
