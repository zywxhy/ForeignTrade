from django.urls import path
from .views import *


urlpatterns = [
    path('branch_sales/',SalesContractView.as_view(),name='branch_sales')
]