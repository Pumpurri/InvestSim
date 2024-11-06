from django.contrib import admin
from .models import Order, Trade

# Register your models here.
@admin.register(Order)
class TradingAdmin(admin.ModelAdmin):
    list_display = ('orderID', 'user', 'stock_symbol',
                    'order_type', 'quantity', 'price',
                    'order_status', 'timestamp')


@admin.register(Trade)
class TradingAdmin(admin.ModelAdmin):
    list_display = ('tradeID', 'order', 'execution_price',
                    'execution_time', 'trade_volume')

