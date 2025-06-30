from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'subject', 'created_at')  # Added phone_number
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone_number', 'subject', 'message')  # Added phone_number