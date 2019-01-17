from django.urls import path
from django.views.generic.base import TemplateView
from invoice.views import InvoiceView,InvoiceAddView,InvoiceModifyView,InvoiceDetailsView

urlpatterns = [
    path('add/',InvoiceAddView.as_view(),name='invoice_add'),
    path('modify/',InvoiceModifyView.as_view(),name='invoice_modify'),
    path('view/',InvoiceView.as_view(),name='invoice_view'),
    path('details/',InvoiceDetailsView.as_view(),name='invoice_details'),

]