from django.urls import path
from .views import DomesticInvoiceViewSet,DomesticInvoiceView


urlpatterns = [
    path('domestic_invoice/operations',DomesticInvoiceView.as_view(),name='domestic_invoice')
]