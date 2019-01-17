from django.urls import path,include
from .views import router,OverseasInvoiceView

urlpatterns = [
    path('overseas_invoice/operations',OverseasInvoiceView.as_view(),name='overseas_invoice'),
]
urlpatterns += router.urls

