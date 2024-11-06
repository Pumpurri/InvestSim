from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import datetime
from django.apps import apps
from decimal import Decimal

# Model representing a user's portfolio
class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50) 
    created_date = models.DateTimeField(auto_now_add=True)
    initial_deposit = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)], default=0.00)
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    cash_balance = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)], default=0.00
        ) 
    total_contributions = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)], default=0.00
        ) 
    
    def save(self, *args, **kwargs):
        # On initial save, set cash balance to initial deposit
        if not self.pk:
            self.cash_balance = Decimal(self.initial_deposit)
            self.total_value = Decimal(self.initial_deposit)
            self.total_contributions = Decimal(self.initial_deposit)
        super().save(*args, **kwargs)
    
    def update_total_value(self):
        # Calculate the total value of the portfolio by summing the value of all holdings and cash balance
        total_holdings_value = Decimal(sum(holding.quantity * holding.current_price for holding in self.holdings.all()))
        self.total_value = total_holdings_value + self.cash_balance
        self.save()

    def calc_cost_basis(self):
        # Calculate the cost basis of the portfolio (total purchase price of holdings)
        total_cost = Decimal(0)
        total_quantity = Decimal(0)
        
        for transaction in self.transactions.filter(type=TransactionType.BUY):
            total_cost += transaction.price * transaction.quantity
            total_quantity += transaction.quantity
        
        # Avoid division by zero
        if total_quantity > 0:
            return total_cost / total_quantity
        return 0

    def total_return(self):
        # Calculate the total return on the portfolio
        cost_basis = self.calc_cost_basis()
        current_value = self.total_value - self.cash_balance    # Calculate ONLY investment value
        if cost_basis > 0:
            return ((current_value - cost_basis) / cost_basis) * 100
        return 0
    
    def annualized_return(self):
        # Calculate the annualized return of the portfolio
        duration = datetime.datetime.now() - self.created_date
        years = duration.days / 365.25

        if years < 1:
            return 0
        
        total_return = self.total_return() / 100
        return (((1 + total_return) ** (1 / years)) - 1) * 100
        
    def risk_metrics(self):
        pass

    def asset_allocation(self):
        pass
    
# Model representing individual holdings within a portfolio
class Holding(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='holdings', on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    # TODO: category = models.CharField(max_length=20) # Optional: Category of the holding to do asset allocation

    @classmethod
    def get_or_create_holding(cls, portfolio, symbol,
                              purchase_price):
        Stock = apps.get_model('stocks', 'Stock')
        try:
            stock = Stock.objects.get(symbol=symbol)
            current_price = stock.current_price
        except Stock.DoesNotExist:
            raise ValidationError(f"Stock with symbol {symbol} does not exist.")
        
        holding, created = cls.objects.get_or_create(
            portfolio=portfolio,
            symbol=symbol,
            defaults={'quantity': 0, 'purchase_price': purchase_price}
        )
        return holding, created

# Choices for transaction types
class TransactionType(models.TextChoices):
    BUY = 'BUY', _('Buy')
    SELL = 'SELL', _('Sell')
    # TODO: DIVIDEND = 'DIVIDEND', _('Dividend')

# Model representing transactions associated with a portfolio
class Transaction(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='transactions', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TransactionType.choices)
    date = models.DateTimeField(auto_now_add=True)
    symbol = models.CharField(max_length=10)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=Decimal('0.00'))

    def save(self, *args, **kwargs):
        if self.price is None:
            Stock = apps.get_model('stocks', 'Stock')
            try:
                stock = Stock.objects.get(symbol=self.symbol)
                self.price = stock.current_price
            except Stock.DoesNotExist:
                raise ValidationError(f"Stock with symbol {self.symbol} does not exist.")

        self.total_amount = self.quantity * self.price
        self.full_clean()
        super().save(*args, **kwargs)

    def update_holding_quantity(self):
        holding, created = Holding.get_or_create_holding(
            portfolio=self.portfolio,
            symbol=self.symbol,
            purchase_price=self.price,
        )
        if self.type == TransactionType.BUY:
            if self.total_amount > self.portfolio.cash_balance:
                raise ValidationError("Total purchase price is more than cash balance.")
            holding.quantity += self.quantity
            self.portfolio.cash_balance -= self.total_amount
        elif self.type == TransactionType.SELL:
            if (holding.quantity - self.quantity) < 0:
                raise ValidationError("Cannot sell more shares than are held.")
            holding.quantity -= self.quantity
            self.portfolio.cash_balance += self.total_amount
        
        holding.save()
        self.portfolio.save()
        self.portfolio.update_total_value()

# Model representing contributions made to a portfolio
class Contribution(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name="contributions", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Update the portfolio's cash balance and total contributions when a new contribution is made
        super().save(*args, **kwargs)
        self.portfolio.cash_balance += self.amount
        self.portfolio.total_contributions += self.amount
        self.portfolio.save()
        self.portfolio.update_total_value()