from django.contrib import admin
from django.utils.safestring import mark_safe  # Add this line
from .models import Tag, Category

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at', 'updated_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    def tag_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')

    tag_image.short_description = 'Image'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at', 'updated_at', 'category_image']
    list_filter = ['is_active']
    prepopulated_fields = {'slug': ('name',)}

    def category_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')

    category_image.short_description = 'Image'
