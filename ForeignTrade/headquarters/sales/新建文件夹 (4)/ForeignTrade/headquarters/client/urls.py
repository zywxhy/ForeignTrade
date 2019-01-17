from django.urls import path
from client.views import ClientView

urlpatterns = [
    path('client/',ClientView.as_view(),name='client'),
    # path('supplier_info/',SupplierInfoView.as_view(),name='supplier_info'),
]
