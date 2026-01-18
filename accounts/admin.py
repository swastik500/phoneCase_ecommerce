from django.contrib import admin
from .models import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):  # Changed from admin.site.ModelAdmin to admin.ModelAdmin
    list_display = ['user', 'full_name', 'city', 'is_default']