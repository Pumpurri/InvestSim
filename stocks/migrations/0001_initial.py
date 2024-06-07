from django.db import migrations, models
import requests

def create_initial_stocks(apps, schema_editor):
    Stock = apps.get_model('stocks', 'Stock')

    initial_stocks = [
        {'symbol': 'AAPL', 'name': 'Apple Inc.'},
        {'symbol': 'MSFT', 'name': 'Microsoft Corp.'},
        {'symbol': 'AMZN', 'name': 'Amazon.com Inc.'},
    ]

    api_key = "lU7kZOh9e7xeHd8HBzYL00jZzaPovqYO"
    for stock_data in initial_stocks:
        symbol = stock_data['symbol']
        url = f'https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={api_key}'

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            current_price = data[0]['price'] if data else 0.0
        except requests.exceptions.RequestException as e:
            print(f"Error fetching current price for {symbol}: {e}")
            current_price = 0.0

        Stock.objects.update_or_create(symbol=stock_data['symbol'], defaults={
            'name': stock_data['name'],
            'current_price': current_price
        })

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('current_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RunPython(create_initial_stocks),
    ]