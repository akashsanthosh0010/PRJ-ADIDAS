from django.contrib import admin
from .models import CustomUser

def block_users(modeladmin, request, queryset):
    queryset.update(is_blocked=True)

def unblock_users(modeladmin, request, queryset):
    queryset.update(is_blocked=False)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_blocked',]
    actions = [block_users, unblock_users]

admin.site.register(CustomUser, CustomUserAdmin)
