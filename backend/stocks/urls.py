from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [

    path('', views.StockList.as_view()),
    path('<int:pk>/', views.StockDetail.as_view()),



    # JSON Response for stock info
    path('stock_gen_info/<str:symbol>/', views.stock_info_json, name='stock_gen_info'),

#     # Template response for stock price
#     path('stock_price/<str:symbol>/', views.stock_price_template_view, name='stock_price_page'),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)
