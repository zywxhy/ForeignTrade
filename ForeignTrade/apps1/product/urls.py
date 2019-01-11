from django.contrib import admin
from django.urls import path,include
from product.views import ProductView,ProductSelectView,get_product
from django.views.static import serve


from django.conf.urls import url
import xadmin

urlpatterns = [
    path('product/<str:search>',ProductView.as_view(),name='product'),
    path('product_select/', ProductSelectView.as_view(), name='product_select'),
    path('get_product/',get_product,name='get_product')
]