# from django.test import TestCase
# import requests
# from unittest.mock import patch
# from stocks.services import fetch_current_price

# class FetchCurrentPriceTests(TestCase):

#     @patch('stocks.services.requests.get')
#     def test_fetch_current_price_success(self, mock_get):
#         mock_response = {
#             "symbol": "AAPL",
#             "price": 150.00
#         }
#         mock_get.return_value.status_code = 200
#         mock_get.return_value.json.return_value = [mock_response]

#         price = fetch_current_price('AAPL')
#         self.assertEqual(price, 150.00)

#     @patch('stocks.services.requests.get')
#     def test_fetch_current_price_failure(self, mock_get):
#         mock_get.return_value.status_code = 404
#         mock_get.return_value.raise_for_status.side_effect = requests.exceptions.RequestException

#         price = fetch_current_price('INVALID')
#         self.assertEqual(price, 0)