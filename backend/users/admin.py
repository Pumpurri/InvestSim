from django.contrib import admin
from .models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class StockAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

