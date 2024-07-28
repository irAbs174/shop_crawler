from django.contrib import admin
from .models import BotUsers, SiteMap, Product, UsProduct

@admin.register(BotUsers)
class BotUsersAdmin(admin.ModelAdmin):
    list_display = ('userId', 'username', 'first_name', 'last_name', 'created_at', 'updated_at')
    search_fields = ('userId', 'username', 'first_name', 'last_name')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(SiteMap)
class SiteMapAdmin(admin.ModelAdmin):
    list_display = ('target', 'siteMapUrl', 'created_at', 'updated_at')
    search_fields = ('target', 'siteMapUrl')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_key', 'product_name', 'product_price', 'product_stock', 'product_status', 'created_at', 'updated_at')
    search_fields = ('product_key', 'product_name', 'product_price')
    list_filter = ('product_status', 'created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(UsProduct)
class UsProductAdmin(admin.ModelAdmin):
    list_display = ('us_product_key', 'us_product_name', 'us_product_price', 'us_product_status', 'created_at', 'updated_at')
    search_fields = ('us_product_key', 'us_product_name', 'us_product_price')
    list_filter = ('us_product_status', 'created_at', 'updated_at')
    ordering = ('-created_at',)
