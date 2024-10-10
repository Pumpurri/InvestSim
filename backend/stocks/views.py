from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Stock

def stock_info_json(request, symbol):
    try:
        stock = Stock.objects.get(symbol=symbol)
        data = {
            'symbol': stock.symbol,
            'name': stock.name,
            'current_price': stock.current_price,
            'last_updated': stock.last_updated,
        }    
        return JsonResponse(data)   
    except Stock.DoesNotExist:
        return JsonResponse({'Error': 'Stock not found'}, status=404)


def stock_price_template_view(request, symbol): 
    stock = get_object_or_404(Stock, symbol=symbol)
    data = {
        'symbol': stock.symbol,
        'name': stock.name,
        'current_price': stock.current_price,
        'last_updated': stock.last_updated,
    }
    return render(request, 'stocks/stock_price.html', data)