from django.urls import path
from purchase.views import PurchaseAddView,PurchaseModifyView,PurchaseDetailsView,PurchaseView


urlpatterns = [
    path('add/',PurchaseAddView.as_view(),name='purchase_add'),
    path('modify/',PurchaseModifyView.as_view(),name='purchase_modify'),
    path('details/',PurchaseDetailsView.as_view(),name='purchase_details'),
    path('view/', PurchaseView.as_view(), name='purchase_view'),

]
