# Django libraries
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Project libraries
from .models import Customer
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.
class CustomerAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Customer
    list_display = ('email', 'is_staff', 'is_active','phone')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'phone')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(Customer, CustomerAdmin)