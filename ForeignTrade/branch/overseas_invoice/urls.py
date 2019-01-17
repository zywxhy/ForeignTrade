from django.urls import path,include
from .views import router,OverseasInvoiceView,OverseasInvoiceViewReview,OverseasInvoiceListView

urlpatterns = [
    path('overseas_invoice/operations',OverseasInvoiceView.as_view(),name='overseas_invoice'),
    path('overseas_invoice/list',OverseasInvoiceListView.as_view(),name='overseas_invoice_list'),
    path('overseas_invoice/review', OverseasInvoiceViewReview.as_view(), name='overseas_invoice_review'),
]
urlpatterns += router.urls

