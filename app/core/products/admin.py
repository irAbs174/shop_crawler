from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('product_key', 'product_name', 'product_price', 'created_at', 'updated_at')
    # Add search functionality
    search_fields = ('product_key', 'product_name', 'product_parent')
    # Add filters for easy navigation
    list_filter = ('created_at', 'updated_at', 'product_parent')
    # Organize form layout in the admin interface
    fieldsets = (
        (None, {
            'fields': ('product_key', 'product_parent', 'product_name', 'product_price')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    # Make the read-only fields for created_at and updated_at
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Product, ProductAdmin)