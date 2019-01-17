from django.shortcuts import render,HttpResponse,get_object_or_404
from django.views import View
from finance.models import ExchangeRate,ActualPayment,ActualReceipts
from sales.models import CollectionPlan
from purchase.models import Payment
from ForeignTrade.my_class import Layui
# Create your views here.

receipt_fields = ['sales__salesman__company__name','sales__sales_num','receipt','receipt_type','receipt_date','remark']
payment_fields = ['purchase__buyer__company__name', 'purchase__purchase_num','payment_amount', 'payment_type', 'payment_date','remark']

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



# 实际收款单和付款单
class CashFlowView(View):
    def get(self,request):
        type = request.GET.get('type',None)
        search = request.GET.get('search',None)
        if type == 'actual_receipt':
            sales_num = request.GET.get('sales_num', None)
            model = ActualReceipts.objects.filter(**search)
            fields = receipt_fields
        elif type == 'actual_payment':
            purchase_num = request.GET.get('purchase_num', None)
            model = ActualPayment.objects.filter(**search)
            fields = payment_fields
        else:
            return HttpResponse('error', )
        layui = Layui(request, model, fields, len(model))
        data = layui.laytable_url()

        return HttpResponse(data,content_type='application/json')

# 计划收款单和付款单
class CashFlowPlanView(View):
    def get(self,request):
        type = request.GET.get('type',None)
        search = request.GET.get('search',None)
        if type == 'actual_receipt':
            sales_num = request.GET.get('sales_num', None)
            model = CollectionPlan.objects.filter(**search)
            fields = receipt_fields
        elif type == 'actual_payment':
            purchase_num = request.GET.get('purchase_num', None)
            model = Payment.objects.filter(**search)
            fields = payment_fields
        else:
            return HttpResponse('error', )
        layui = Layui(request, model, fields, len(model))
        data = layui.laytable_url()

        return HttpResponse(data,content_type='application/json')


#预计收支表
pass