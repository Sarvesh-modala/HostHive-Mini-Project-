from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Enhanced admin interface for Category model"""
    list_display = ('name', 'host', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'host')
    search_fields = ('name', 'description', 'host__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('name', 'description', 'host')}),
        ('Media', {'fields': ('background_video', 'image')}),
        ('Status', {'fields': ('is_active',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )