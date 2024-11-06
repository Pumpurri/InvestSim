from rest_framework import serializers
from .models import Order, Trade


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['orderID', 'user', 'stock_symbol', 'order_type',
                 'quantity', 'price', 'order_status', 'timestamp']
        

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ['tradeID', 'order', 'execution_price', 
                 'execution_time', 'trade_volume',]
        