from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import F, Sum
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class PortfolioManager(models.Manager):
    def create_portfolio(self, user, name, initial_deposit=Decimal('0.00')):
        if initial_deposit < Decimal('0.00'):
            raise ValidationError("Initial deposit cannot be negative")
            
        return self.create(
            user=user,
            name=name,
            initial_deposit=initial_deposit,
            cash_balance=initial_deposit,
            total_value=initial_deposit,
            total_contributions=initial_deposit
        )

class Portfolio(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='portfolios'
    )
    name = models.CharField(max_length=50, db_index=True)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    initial_deposit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    total_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )
    cash_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )
    total_contributions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )

    objects = PortfolioManager()

    class Meta:
        unique_together = ('user', 'name')
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.user.email}'s {self.name} Portfolio"

    def update_total_value(self):
        try:
            holdings_value = self.holdings.aggregate(
                total=Sum(F('quantity') * F('current_price')))
            total_holdings = holdings_value['total'] or Decimal('0.00')
            self.total_value = total_holdings + self.cash_balance
            self.save(update_fields=['total_value'])
        except Exception as e:
            logger.error(f"Error updating portfolio {self.id} value: {str(e)}")
            raise

    def get_cost_basis(self):
        return self.transactions.filter(
            type=Transaction.TransactionType.BUY
        ).aggregate(
            total=Sum(F('quantity') * F('price'))
        )['total'] or Decimal('0.00')

    def get_total_return(self):
        cost_basis = self.get_cost_basis()
        if cost_basis == Decimal('0.00'):
            return Decimal('0.00')
        return ((self.total_value - cost_basis) / cost_basis) * 100

class HoldingManager(models.Manager):
    def get_holding(self, portfolio, symbol):
        return self.get_queryset().get(
            portfolio=portfolio,
            symbol=symbol.upper()
        )

class Holding(models.Model):
    portfolio = models.ForeignKey(
        Portfolio,
        related_name='holdings',
        on_delete=models.CASCADE
    )
    symbol = models.CharField(max_length=10, db_index=True)
    quantity = models.PositiveIntegerField(default=0)
    average_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    objects = HoldingManager()

    class Meta:
        unique_together = ('portfolio', 'symbol')
        ordering = ['symbol']

    @property
    def current_price(self):
        from .services import get_current_price  # Circular import protection
        return get_current_price(self.symbol)

    @property
    def market_value(self):
        return Decimal(self.quantity) * self.current_price

    @property
    def unrealized_gain(self):
        return (self.current_price - self.average_cost) * self.quantity

    def update_average_cost(self, new_quantity, new_price):
        total_cost = (self.quantity * self.average_cost) + (new_quantity * new_price)
        total_shares = self.quantity + new_quantity
        self.average_cost = total_cost / total_shares
        self.save()

class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        BUY = 'BUY', 'Buy'
        SELL = 'SELL', 'Sell'
        DIVIDEND = 'DIVIDEND', 'Dividend'
        SPLIT = 'SPLIT', 'Stock Split'

    portfolio = models.ForeignKey(
        Portfolio,
        related_name='transactions',
        on_delete=models.CASCADE
    )
    type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
        db_index=True
    )
    symbol = models.CharField(max_length=10, db_index=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    date = models.DateTimeField(default=timezone.now, db_index=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['portfolio', 'date']),
            models.Index(fields=['symbol', 'type']),
        ]

    @property
    def total_amount(self):
        return self.quantity * self.price

    def clean(self):
        if self.price <= Decimal('0.00'):
            raise ValidationError({'price': 'Price must be positive'})
        
        if self.type == Transaction.TransactionType.SELL:
            holding = self.portfolio.holdings.filter(symbol=self.symbol).first()
            if not holding or holding.quantity < self.quantity:
                raise ValidationError(
                    {'quantity': 'Not enough shares to sell'}
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class ContributionManager(models.Manager):
    def contribute(self, portfolio, amount):
        if amount <= Decimal('0.00'):
            raise ValidationError("Contribution amount must be positive")
            
        return self.create(
            portfolio=portfolio,
            amount=amount
        )

class Contribution(models.Model):
    portfolio = models.ForeignKey(
        Portfolio,
        related_name='contributions',
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    date = models.DateTimeField(default=timezone.now, db_index=True)

    objects = ContributionManager()

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            Portfolio.objects.filter(pk=self.portfolio.pk).update(
                cash_balance=F('cash_balance') + self.amount,
                total_contributions=F('total_contributions') + self.amount,
                total_value=F('total_value') + self.amount
            )