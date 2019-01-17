from django.urls import path
from .views import *


urlpatterns = [
    path('branch_stock/operations',BranchStockView.as_view(),name='branch_stock'),
    path('warehousing_result/',WarehousingReview.as_view(),name='warehousing_result'),
    path('invoice_result/',InvoiceReview.as_view(),name='invoice_result')
]