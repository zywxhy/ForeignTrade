from django.shortcuts import render,HttpResponse
from django.views import View
from purchase.forms import PurchaseForm
from purchase.models import PurchaseContract,PurchaseProduct
from sales.models import SalesContract,SalesProduct
from ForeignTrade.my_class import DataSplit,ContractOperations
from itertools import chain
from django.db.models import F
# Create your views here.
errors = {
     0:'添加成功',
     1:'合同重复',
     2:'合同填写错误',
     3:'产品添加错误',

}







class PurchaseView(View):
    def get(self,request):
        user = request.user
        sales_contract = SalesContract.objects.filter(salesman__company__name='润州光电')
        purchase = PurchaseContract.objects.filter(buyer__company__id=user.company_id)
        return (request, 'purchase/purchase_view.html', locals())


class PurchaseAddView(View):
    def get(self,request):
        user = request.user
        sales_num = request.GET.get('sales_num','')
        form = PurchaseForm(request,initial={'sales_num':sales_num})
        #sales_product_list = request.POST.get('sales_product_list').split('@*')
        try:
            sales_id = SalesContract.objects.get(sales_num =sales_num).id
        except:
            sales_id = 9999999
        print(sales_id)
        product_list = SalesProduct.objects.filter(sales_id=sales_id, count__gt=F('outbound_count'))
        products = SalesProduct.sales_serializers(product_list)
        print(products)

        return render(request, 'purchase/purchase_add.html', locals())


    def post(self,request):
        user = request.user
        form = PurchaseForm(user,request.POST)
        #product_split = DataSplit(request.POST['invoice_product'], ['product_id', 'remark', 'count', 'unit_price'],InvoiceProduct)
        contract_operations = ContractOperations(Invoice, form, sub_split1=product_split, )
        product_split = DataSplit(request.POST['purchase_product'],['product_id', 'remark', 'count', 'unit_price', 'amount'], )
        contract_operations = ContractOperations(PurchaseContract, form, sub_split1=product_split,)
        contract_operations.contract_add('purchase_id')
        return HttpResponse(errors[contract_operations.error_index])


class PurchaseModifyView(View):
    def get(self,request):
        sales_num = request.POST.get('sales_num','')
        purchase_num = request.POST.get('purchase_num','')
        purchase_contract = PurchaseContract.objects.get(purchase_num=purchase_num)
        initial = {}
        for key in PurchaseForm(request).fields:
            initial[key] = getattr(purchase_contract,key)
        form = PurchaseForm(request,initial=initial)
        sales_product_list = request.POST.get('sales_product_list').split('@*')
        product = SalesProduct.objects.filter(id=99999999)
        for sales_product in sales_product_list:
            product = chain(product,SalesProduct.objects.filter(sales__sales_num=sales_num,product__product_id=sales_product))
        return render(request, 'purchase/purchase_add.html', locals())


    def post(self,request):
        form = PurchaseForm(request,request.POST)
        pk = PurchaseContract.objects.get(purchase_num=request.POST['purchase_num']).id
        product_split = DataSplit(eval(request.POST['purchase_product']),['product_id', 'remark', 'count', 'unit_price', 'amount'], 7, PurchaseProduct.objects)
        contract_operations = ContractOperations(PurchaseContract, form, sub_split1=product_split,)
        contract_operations.contract_modify(pk,'purchase_id')
        return HttpResponse(errors[contract_operations.error_index])


class PurchaseDetailsView(View):
    def get(self,request):
        purchase_num = request.POST.get('purchase_num','')
        purchase_contract = PurchaseContract.objects.get(purchase_num=purchase_num)
        initial = {}
        for key in PurchaseForm(request).fields:
            initial[key] = getattr(purchase_contract,key)
        form = PurchaseForm(request,initial=initial)
        product_list = PurchaseContract.objects.filter(purchase_num=purchase_num)
        return render(request, 'purchase/purchase_add.html', locals())








