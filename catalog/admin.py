from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):  # Changed to admin.ModelAdmin
    list_display = ['name', 'slug', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):  # Changed to admin.ModelAdmin
    list_display = ['name', 'category', 'price', 'stock', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description_short']
    prepopulated_fields = {'slug': ('name',)}