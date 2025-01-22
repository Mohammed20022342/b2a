from django.contrib import admin
from .models import ContactMessage

# Register your models here.
from .models import Category, Product, Review

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at')
    ordering = ('-created_at',)
    search_fields = ('subject', 'message')