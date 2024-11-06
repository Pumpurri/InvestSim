from rest_framework import serializers
from .models import Portfolio, Holding, Transaction, Contribution


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['user', 'name', 'created_date', 'initial_deposit',
                 'total_value', 'cash_balance', 'total_contributions',]
        

class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holding
        fields = ['portfolio', 'symbol', 'quantity', 
                 'purchase_price', 'current_price',]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['portfolio', 'type', 'date', 'symbol',
                 'quantity', 'price', 'total_amount',]


class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ['portfolio', 'amount', 'date']