from django.contrib import admin
from .models import ContactMessage

# Register your models here.
from .models import Category, Product, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "name_ar")
    save_on_top = True  # Enables save buttons at the top

admin.site.register(Product)
admin.site.register(Review)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at')
    ordering = ('-created_at',)
    search_fields = ('subject', 'message')