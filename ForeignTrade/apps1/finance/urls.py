from django.urls import path,include
from finance.views import get_exchange_rate





urlpatterns = [
    path('get_exchange_rate/',get_exchange_rate,name='get_exchange_rate'),


]