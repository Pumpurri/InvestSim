# from django.test import TestCase
# from django.core.exceptions import ValidationError
# from django.contrib.auth import get_user_model
# from datetime import date
# from .models import Order, Trade, OrderType, OrderStatus

# # Create your tests here.
# from django.test import TestCase
# from django.core.exceptions import ValidationError
# from django.conf import settings
# from .models import Order, Trade, OrderType, OrderStatus

# class OrderModelTest(TestCase):

#     def setUp(self):
#         User = get_user_model()
#         self.user = User.objects.create_user(username='testuser', password='12345', date_of_birth=date(2000, 1, 1))

#     def test_order_creation(self):
#         # Test creating an order with valid data
#         order = Order.objects.create(
#             user=self.user,
#             stock_symbol='AAPL',
#             order_type=OrderType.BUY,
#             quantity=10,
#             price=150.00
#         )
#         self.assertEqual(order.user.username, 'testuser')
#         self.assertEqual(order.stock_symbol, 'AAPL')
#         self.assertEqual(order.order_type, OrderType.BUY)
#         self.assertEqual(order.quantity, 10)
#         self.assertEqual(order.price, 150.00)
#         self.assertEqual(order.order_status, OrderStatus.OPEN)

#     def test_order_negative_quantity(self):
#         # Test creating an order with a negative quantity (should raise ValidationError)
#         with self.assertRaises(ValidationError):
#             order = Order(
#                 user=self.user,
#                 stock_symbol='AAPL',
#                 order_type=OrderType.BUY,
#                 quantity=-10,
#                 price=150.00
#             )
#             order.full_clean() 

#     def test_order_zero_price(self):
#         # Test creating an order with a zero price (should raise ValidationError)
#         with self.assertRaises(ValidationError):
#             order = Order(
#                 user=self.user,
#                 stock_symbol='AAPL',
#                 order_type=OrderType.BUY,
#                 quantity=10,
#                 price=0.00
#             )
#             order.full_clean()  



# class TradeModelTest(TestCase):

#     def setUp(self):
#         User = get_user_model()
#         self.user = User.objects.create_user(username='testuser', password='12345', date_of_birth=date(2000, 1, 1))
#         self.order = Order.objects.create(
#             user=self.user,
#             stock_symbol='AAPL',
#             order_type=OrderType.BUY,
#             quantity=10,
#             price=150.00
#         )

#     def test_trade_creation(self):
#         # Test creating a trade with valid data
#         trade = Trade.objects.create(
#             order=self.order,
#             execution_price=150.00,
#             trade_volume=10
#         )
#         self.assertEqual(trade.order, self.order)
#         self.assertEqual(trade.execution_price, 150.00)
#         self.assertEqual(trade.trade_volume, 10)

#     def test_trade_negative_execution_price(self):
#         # Test creating a trade with a negative execution price (should raise ValidationError)
#         with self.assertRaises(ValidationError):
#             trade = Trade(
#                 order=self.order,
#                 execution_price=-150.00,
#                 trade_volume=10
#             )
#             trade.full_clean() 

#     def test_trade_zero_trade_volume(self):
#         # Test creating a trade with a zero trade volume (should raise ValidationError)
#         with self.assertRaises(ValidationError):
#             trade = Trade(
#                 order=self.order,
#                 execution_price=150.00,
#                 trade_volume=0
#             )
#             trade.full_clean() 

#     def test_create_order_with_different_order_types(self):
#         order_buy = Order.objects.create(
#             user=self.user,
#             stock_symbol='AAPL',
#             order_type=OrderType.BUY,
#             quantity=10,
#             price=150.00
#         )
#         order_sell = Order.objects.create(
#             user=self.user,
#             stock_symbol='AAPL',
#             order_type=OrderType.SELL,
#             quantity=10,
#             price=150.00
#         )
#         order_short_sell = Order.objects.create(
#             user=self.user,
#             stock_symbol='AAPL',
#             order_type=OrderType.SHORT_SELL,
#             quantity=10,
#             price=150.00
#         )
#         self.assertEqual(order_buy.order_type, OrderType.BUY)
#         self.assertEqual(order_sell.order_type, OrderType.SELL)
#         self.assertEqual(order_short_sell.order_type, OrderType.SHORT_SELL)

#     def test_update_order_status(self):
#         order = Order.objects.create(
#             user=self.user,
#             stock_symbol='AAPL',
#             order_type=OrderType.BUY,
#             quantity=10,
#             price=150.00
#         )
#         order.order_status = OrderStatus.FILLED
#         order.save()
#         updated_order = Order.objects.get(orderID=order.orderID)
#         self.assertEqual(updated_order.order_status, OrderStatus.FILLED)

#     def test_create_trade_with_different_execution_prices(self):
#         trade1 = Trade.objects.create(
#             order=self.order,
#             execution_price=150.00,
#             trade_volume=10
#         )
#         trade2 = Trade.objects.create(
#             order=self.order,
#             execution_price=155.00,
#             trade_volume=10
#         )
#         trade3 = Trade.objects.create(
#             order=self.order,
#             execution_price=160.00,
#             trade_volume=10
#         )
#         self.assertEqual(trade1.execution_price, 150.00)
#         self.assertEqual(trade2.execution_price, 155.00)
#         self.assertEqual(trade3.execution_price, 160.00)
