from django.urls import path
from .views import DomesticInvoiceListView,DomesticInvoiceView


urlpatterns = [
    path('domestic_invoice/operations',DomesticInvoiceView.as_view(),name='domestic_invoice'),
    path('domestic_invoice/list', DomesticInvoiceListView.as_view(), name='domestic_invoice_list'),


]