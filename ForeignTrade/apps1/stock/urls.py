from django.urls import path
from stock.views import StockView,StockReviewView,StockRecordView,get_stock_product

urlpatterns = [
    path('get_stock_product/',get_stock_product,name='get_stock_product'),
    path('stock/',StockView.as_view(),name='stock'),
    path('stock_review/',StockReviewView.as_view(),name='stock_review'),
    path('stock_record/',StockRecordView.as_view(),name='stock_record'),
]