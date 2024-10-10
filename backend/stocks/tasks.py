from celery import shared_task
import requests
from .models import Stock
from math import ceil

companies = [
    {'symbol': 'AAPL', 'name': 'Apple Inc.'},
    {'symbol': 'MSFT', 'name': 'Microsoft Corp.'},
    {'symbol': 'GOOGL', 'name': 'Alphabet Inc.'},
    {'symbol': 'AMZN', 'name': 'Amazon.com Inc.'},
    {'symbol': 'META', 'name': 'Meta Platforms Inc.'},
    {'symbol': 'NVDA', 'name': 'NVIDIA Corp.'},
    {'symbol': 'IBM', 'name': 'IBM (International Business Machines Corp.)'},
    {'symbol': 'ADBE', 'name': 'Adobe Inc.'},
    {'symbol': 'CRM', 'name': 'Salesforce Inc.'},
    {'symbol': 'ORCL', 'name': 'Oracle Corp.'},
    {'symbol': 'NOW', 'name': 'ServiceNow Inc.'},
    {'symbol': 'PLTR', 'name': 'Palantir Technologies Inc.'},
    {'symbol': 'SAP', 'name': 'SAP SE'},
    {'symbol': 'CSCO', 'name': 'Cisco Systems Inc.'},
    {'symbol': 'TSLA', 'name': 'Tesla Inc.'},
    {'symbol': 'INTC', 'name': 'Intel Corp.'},
    {'symbol': 'AMD', 'name': 'Advanced Micro Devices Inc.'},
    {'symbol': 'QCOM', 'name': 'Qualcomm Inc.'},
    {'symbol': 'AVGO', 'name': 'Broadcom Inc.'},
    {'symbol': 'V', 'name': 'Visa Inc.'},

    {'symbol': 'MA', 'name': 'Mastercard Inc.'},
    {'symbol': 'PYPL', 'name': 'PayPal Holdings Inc.'},
    {'symbol': 'SQ', 'name': 'Block Inc.'},
    {'symbol': 'HOOD', 'name': 'Robinhood Markets Inc.'},
    {'symbol': 'NFLX', 'name': 'Netflix Inc.'},
    {'symbol': 'SPOT', 'name': 'Spotify Technology S.A.'},
    {'symbol': 'EA', 'name': 'Electronic Arts Inc.'},
    {'symbol': 'U', 'name': 'Unity Software Inc.'},
    {'symbol': 'TTWO', 'name': 'Take-Two Interactive Software Inc.'},
    {'symbol': 'NET', 'name': 'Cloudflare Inc.'},
    {'symbol': 'SNOW', 'name': 'Snowflake Inc.'},
    {'symbol': 'CRWD', 'name': 'CrowdStrike Holdings Inc.'},
    {'symbol': 'MDB', 'name': 'MongoDB Inc.'},
    {'symbol': 'RIVN', 'name': 'Rivian Automotive Inc.'},
    {'symbol': 'LCID', 'name': 'Lucid Group Inc.'},
    {'symbol': 'NKLA', 'name': 'Nikola Corp.'},
    {'symbol': 'UBER', 'name': 'Uber Technologies Inc.'},
    {'symbol': 'LYFT', 'name': 'Lyft Inc.'},
    {'symbol': 'SNAP', 'name': 'Snap Inc.'},
    {'symbol': 'PINS', 'name': 'Pinterest Inc.'},

    {'symbol': 'AI', 'name': 'C3.ai Inc.'},
    {'symbol': 'PATH', 'name': 'UiPath Inc.'},
    {'symbol': 'WMT', 'name': 'Walmart Inc.'},
    {'symbol': 'HD', 'name': 'The Home Depot Inc.'},
    {'symbol': 'COST', 'name': 'Costco Wholesale Corp.'},
    {'symbol': 'PEP', 'name': 'PepsiCo Inc.'},
    {'symbol': 'KO', 'name': 'Coca-Cola Co.'},
    {'symbol': 'NKE', 'name': 'Nike Inc.'},
    {'symbol': 'F', 'name': 'Ford Motor Co.'},
    {'symbol': 'GM', 'name': 'General Motors Co.'},
    {'symbol': 'TM', 'name': 'Toyota Motor Corp.'},
    {'symbol': 'BRK.B', 'name': 'Berkshire Hathaway Inc.'},
    {'symbol': 'GS', 'name': 'Goldman Sachs Group Inc.'},
    {'symbol': 'MS', 'name': 'Morgan Stanley'},
    {'symbol': 'C', 'name': 'Citigroup Inc.'},
    {'symbol': 'JPM', 'name': 'JPMorgan Chase & Co.'},
    {'symbol': 'JNJ', 'name': 'Johnson & Johnson'},
    {'symbol': 'PFE', 'name': 'Pfizer Inc.'},
    {'symbol': 'LLY', 'name': 'Eli Lilly and Co.'},
    {'symbol': 'ABBV', 'name': 'AbbVie Inc.'},

    {'symbol': 'MRK', 'name': 'Merck & Co. Inc.'},
    {'symbol': 'XOM', 'name': 'Exxon Mobil Corp.'},
    {'symbol': 'CVX', 'name': 'Chevron Corp.'},
    {'symbol': 'NEE', 'name': 'NextEra Energy Inc.'},
    {'symbol': 'DUK', 'name': 'Duke Energy Corp.'},
    {'symbol': 'FDX', 'name': 'FedEx Corp.'},
    {'symbol': 'UPS', 'name': 'United Parcel Service Inc.'},
    {'symbol': 'BA', 'name': 'Boeing Co.'},
    {'symbol': 'LMT', 'name': 'Lockheed Martin Corp.'},
    {'symbol': 'GE', 'name': 'General Electric Co.'},
    {'symbol': 'MMM', 'name': '3M Co.'},
    {'symbol': 'HON', 'name': 'Honeywell International Inc.'},
    {'symbol': 'T', 'name': 'AT&T Inc.'},
    {'symbol': 'VZ', 'name': 'Verizon Communications Inc.'},
    {'symbol': 'TMUS', 'name': 'T-Mobile US Inc.'},
    {'symbol': 'DIS', 'name': 'Walt Disney Co.'},
    {'symbol': 'CMCSA', 'name': 'Comcast Corp.'},
    {'symbol': 'ADP', 'name': 'Automatic Data Processing Inc.'},
    {'symbol': 'BK', 'name': 'Bank of New York Mellon Corp.'},
    {'symbol': 'SCHW', 'name': 'Charles Schwab Corp.'},
]

def batch_companies(companies, batch_size=20):
    num_batches = ceil(len(companies) / batch_size)
    return [companies[i*batch_size: (i+1)*batch_size] for i in range(num_batches)]

@shared_task
def fetch_stock_prices():
    batches = batch_companies(companies, batch_size=20)
    api_key = "lU7kZOh9e7xeHd8HBzYL00jZzaPovqYO"

    for batch in batches:
        symbols = ','.join([company['symbol'] for company in batch])
        url = f'https://financialmodelingprep.com/api/v3/quote/{symbols}?apikey={api_key}'

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching stock data for {symbols}: {e}")
            continue

        for company, stock_info in zip(batch, data):
            symbol = company['symbol']
            current_price = stock_info.get('price', 0.0)

            Stock.objects.update_or_create(
                symbol=symbol,
                defaults={'name': company['name'], 'current_price': current_price}
            )

        print(f"Updated stock prices for batch: {symbols}")