from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from .models import Portfolio, Holding, Transaction, TransactionType
from django.core.exceptions import ValidationError

class TransactionModelTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password',
            date_of_birth=date(2000, 1, 1)
        )
        self.portfolio = Portfolio.objects.create(user=self.user, name='Test Portfolio', initial_deposit=5000.00)

    def test_update_holding_quantity_buy(self):
        transaction = Transaction.objects.create(
            portfolio=self.portfolio,
            type=TransactionType.BUY,
            symbol='AAPL',
            quantity=10,
            price=150.00,
            total_amount=1500.00
        )

        transaction.update_holding_quantity()
        holding = Holding.objects.get(portfolio=self.portfolio, symbol='AAPL')

        self.assertEqual(holding.quantity, 10)
        self.assertEqual(holding.purchase_price, 150.00)
        self.assertEqual(self.portfolio.cash_balance, 3500.00)
        self.assertEqual(self.portfolio.total_value, 3500.00 + 10 * 150.00)

    def test_update_holding_quantity_sell(self):
        holding = Holding.objects.create(
            portfolio=self.portfolio,
            symbol='AAPL',
            quantity=20,
            purchase_price=150.00,
            current_price=150.00
        )

        transaction = Transaction.objects.create(
            portfolio=self.portfolio,
            type=TransactionType.SELL,
            symbol='AAPL',
            quantity=5,
            price=150.00,
            total_amount=750.00
        )

        transaction.update_holding_quantity()
        holding.refresh_from_db()
        self.assertEqual(holding.quantity, 15)
        self.assertEqual(self.portfolio.cash_balance, 5000.00 + 750.00)
        self.assertEqual(self.portfolio.total_value, 5000.00 + 750.00 + 15 * 150.00)

    # def test_buy_transaction_exceeds_cash_balance(self):
    #     transaction = Transaction.objects.create(
    #         portfolio=self.portfolio,
    #         type=TransactionType.BUY,
    #         symbol='AAPL',
    #         quantity=100,
    #         price=150.00,
    #         total_amount=15000.00
    #     )

    #     with self.assertRaises(ValidationError):
    #         transaction.update_holding_quantity()

    # def test_sell_transaction_exceeds_holding_quantity(self):
    #     holding = Holding.objects.create(
    #         portfolio=self.portfolio,
    #         symbol='AAPL',
    #         quantity=10,
    #         purchase_price=150.00,
    #         current_price=150.00
    #     )

    #     transaction = Transaction.objects.create(
    #         portfolio=self.portfolio,
    #         type=TransactionType.SELL,
    #         symbol='AAPL',
    #         quantity=20,
    #         price=150.00,
    #         total_amount=3000.00
    #     )

    #     with self.assertRaises(ValidationError):
    #         transaction.update_holding_quantity()