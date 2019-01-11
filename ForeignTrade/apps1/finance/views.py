from django.shortcuts import render,HttpResponse
from finance.models import ExchangeRate
# Create your views here.


# 返回汇率
def get_exchange_rate(request):
    currency = request.GET['currency']
    print(currency)
    user = request.user
    if user.company.name == '润州光电':
        exchange_rate = ExchangeRate.objects.get(type='CNY',currency=currency)
    else:
        exchange_rate = ExchangeRate.objects.get(type='USD', currency=currency)
    return HttpResponse(exchange_rate.exchange_rate)




