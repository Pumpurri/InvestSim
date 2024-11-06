from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.OrderList.as_view()),
    path('order/<int:pk>/', views.OrderDetail.as_view()),
    path('trade/', views.TradeList.as_view()),
    path('trade/<int:pk>/', views.TradeDetail.as_view()),
]