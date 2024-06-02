from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator

# Define the possible statuses for an order
class OrderStatus(models.TextChoices):
    OPEN = 'OP', _('Open')
    FILLED = 'FI', _('Filled')
    CANCELLED = 'CA', _('Cancelled')

# Define the possible types of an order
class OrderType(models.TextChoices):
    BUY = 'BUY', _('Buy')
    SELL = 'SELL', _('Sell')
    SHORT_SELL = 'SHORT_SELL', _('Short Sell')

# Model representing an Order
class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=10)
    order_type = models.CharField(
        max_length=10,
        choices=OrderType.choices,
        help_text='Type of the order'
    )
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    order_status = models.CharField (
        max_length=2,
        choices=OrderStatus.choices,
        default=OrderStatus.OPEN,
        help_text='Current status of the order'
    )
    timestamp = models.DateTimeField(auto_now_add=True)

# Model representing a Trade
class Trade(models.Model):
    tradeID = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    execution_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    execution_time = models.DateTimeField(auto_now_add=True)
    trade_volume = models.IntegerField(validators=[MinValueValidator(1)])

