from django.urls import path
from . import views

urlpatterns = [
    # JSON Response for stock info
    path('stock_gen_info/<str:symbol>/', views.stock_info_json, name='stock_gen_info'),

    # Template response for stock price
    path('stock_price/<str:symbol>/', views.stock_price_template_view, name='stock_price_page'),
    
]
