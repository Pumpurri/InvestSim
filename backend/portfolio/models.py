from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import datetime

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
            self.cash_balance = self.initial_deposit
        super().save(*args, **kwargs)
    
    def update_total_value(self):
        # Calculate the total value of the portfolio by summing the value of all holdings and cash balance
        print("TESTING UPDATE TV")
        print("Calculating total value of portfolio")
        total_holdings_value = float(sum(holding.quantity * holding.current_price for holding in self.holdings.all()))
        print(f"Total holdings value: {total_holdings_value}. also: {type(total_holdings_value)}")
        print(f"Cash balance: {self.cash_balance}. also: {type(self.cash_balance)}")
        self.total_value = total_holdings_value + self.cash_balance
        print(f"Updated total value: {self.total_value}")
        self.save()

    def calc_cost_basis(self):
        # Calculate the cost basis of the portfolio (total purchase price of holdings)
        cost_basis = sum(holding.quantity * holding.purchase_price for holding in self.holdings.all())
        return cost_basis

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

    # def asset_allocation(self):
    #     pass
    
# Model representing individual holdings within a portfolio
class Holding(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='holdings', on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2) 
    # TODO: category = models.CharField(max_length=20) # Optional: Category of the holding to do asset allocation

    @classmethod
    def get_or_create_holding(cls, portfolio, symbol,
                              purchase_price, current_price):
        # Get or create a holding for a given portfolio and stock symbol
        holding, created = cls.objects.get_or_create(
            portfolio=portfolio,
            symbol=symbol,
            defaults={'quantity': 0, 'purchase_price': purchase_price, 'current_price': current_price}
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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def update_holding_quantity(self):
        # Update the holding quantity based on the transaction type (buy/sell)
        holding, created = Holding.get_or_create_holding(
            portfolio=self.portfolio,
            symbol=self.symbol,
            purchase_price=self.price,
            current_price=self.get_current_market_price(self.symbol) # Revise to actual functionality
        )
        if self.type == TransactionType.BUY:
            print("TESTING UPDATE HOLDING QUANTITY BUY")
            print(f"Type of self.quantity: {type(self.quantity)}")
            print(f"Type of self.price: {type(self.price)}")
            if (self.quantity * self.price) > self.portfolio.cash_balance:
                # print(f"ValidationError: Total purchase price xxx is more than cash balance ({self.portfolio.cash_balance})")
                raise ValidationError("Total purchase price is more than cash balance.")
            holding.quantity += self.quantity
            self.portfolio.cash_balance -= self.total_amount
        elif self.type == TransactionType.SELL:
            print("\nTESTING UPDATE HOLDING QUANTITY SELL")
            print(f"Type of holding.quantity: {type(holding.quantity)}")
            print(f"Type of self.quantity: {type(self.quantity)}")
            if (holding.quantity - self.quantity) < 0:
                # print(f"ValidationError: Cannot sell more shares ({self.quantity}) than are held ({holding.quantity})")
                raise ValidationError("Cannot sell more shares than are held.")
            holding.quantity -= self.quantity
            self.portfolio.cash_balance += self.total_amount
        
        holding.save()
        self.portfolio.save()
        self.portfolio.update_total_value()

    def get_current_market_price(self,symbol):
        return 150.00   # revise to actual functionality

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