from django.urls import path
from . import views

urlpatterns = [
    path('portfolio/', views.PortfolioList.as_view()),
    path('portfolio/<int:pk>/', views.PortfolioDetail.as_view()),
    path('holding/', views.HoldingList.as_view()),
    path('holding/<int:pk>/', views.HoldingDetail.as_view()),
    path('transaction/', views.TransactionList.as_view()),
    path('transaction/<int:pk>/', views.TransactionDetail.as_view()),
    path('contribution/', views.ContributionList.as_view()),
    path('contribution/<int:pk>/', views.ContributionDetail.as_view()),
]