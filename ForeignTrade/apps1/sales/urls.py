from django.urls import path
from django.views.generic.base import TemplateView
from sales.views import SalesAddView,SalesContractView,SalesDetailsView,SalesContractModify,get_sales_info,SalesProductView,SalesProdcutListView

urlpatterns = [
    path('add/',SalesAddView.as_view(),name='sales_add'),
    path('modify/',SalesContractModify.as_view(),name='sales_modify'),
    path('view/',SalesContractView.as_view(),name='sales_view'),
    path('details/',SalesDetailsView.as_view(),name='sales_details'),
    path('get_sales_info/', get_sales_info, name='get_sales_info'),
    path('sales_product/', SalesProductView.as_view(), name='sales_product'),
    path('sales_list/', SalesProdcutListView.as_view(), name='sales_list'),
]