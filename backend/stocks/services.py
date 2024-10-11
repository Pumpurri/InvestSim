import requests
from .models import Stock
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_current_price(symbol): 
    api_key = os.getenv('API_KEY')
    url = f'https://financialmodelingprep.com/api/v3/quote/{symbol}/?apikey={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data:
            return data[0]['price']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching current price for {symbol}: {e}")
    return 0