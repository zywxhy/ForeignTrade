from django.urls import path
from supplier.views import *

urlpatterns = [
    path('supplier/',SupplierView.as_view(),name='supplier'),
    path('supplier_info/',SupplierInfoView.as_view(),name='supplier_info'),
]
