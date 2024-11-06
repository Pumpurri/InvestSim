from rest_framework import generics, status
from .models import Stock
from .serializers import StockSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response

class StockList(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class StockDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

@api_view(['GET'])
def stock_info_json(request, symbol):
    """
    Retrieve stock information by symbol.
    """
    try:
        stock = Stock.objects.get(symbol__iexact=symbol)
    except Stock.DoesNotExist:
        return Response({'error': 'Stock not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = StockSerializer(stock)
    return Response(serializer.data, status=status.HTTP_200_OK)
