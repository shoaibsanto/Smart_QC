from django.contrib import admin
from .models import Factory

@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'latitude', 'longitude')
    search_fields = ('name', 'address')
