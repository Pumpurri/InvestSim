from django.contrib import admin
from .models import Portfolio, Holding, Transaction, Contribution

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'total_value', 'cash_balance', 'created_date')

@admin.register(Holding)
class HoldingAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'symbol', 'quantity', 'purchase_price')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'type', 'symbol', 'quantity', 'price', 'total_amount', 'date')

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'amount', 'date')