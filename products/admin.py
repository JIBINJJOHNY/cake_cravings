from django.contrib import admin
from django.utils.safestring import mark_safe  
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_image', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active']
    prepopulated_fields = {'slug': ('name',)}

    def category_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
    category_image.short_description = 'Image'
