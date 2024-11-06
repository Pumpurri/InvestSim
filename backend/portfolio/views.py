# Create your views here.
from rest_framework import generics
from .models import Portfolio, Holding, Transaction, Contribution
from .serializers import PortfolioSerializer, HoldingSerializer, TransactionSerializer, ContributionSerializer


"""
Portfolio 
"""
class PortfolioList(generics.ListAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

class PortfolioDetail(generics.RetrieveAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer


"""
Holding 
"""
class HoldingList(generics.ListAPIView):
    queryset = Holding.objects.all()
    serializer_class = HoldingSerializer

class HoldingDetail(generics.RetrieveAPIView):
    queryset = Holding.objects.all()
    serializer_class = HoldingSerializer


"""
Transaction 
"""
class TransactionList(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class TransactionDetail(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


"""
Contribution 
"""
class ContributionList(generics.ListAPIView):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer

class ContributionDetail(generics.RetrieveAPIView):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer