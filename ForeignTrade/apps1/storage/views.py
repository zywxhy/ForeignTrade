from django.shortcuts import render,HttpResponse
from django.views import View
from storage.forms import StorageAddForm
from storage.models import Storage,StorageProduct
from purchase.models import PurchaseProduct
from django.db.models import F
from itertools import chain
from ForeignTrade.my_class import DataSplit,ContractOperations
# Create your views here.

errors = {
     0:'添加成功',
     1:'合同重复',
     2:'合同填写错误',
     3:'产品添加错误',

}

class StorageView(View):
    pass



class StorageAddView(View):
    def get(self,request):
        user = request.user
        form = StorageAddForm(request)
        purchase_num = request.POST.get('purchase_num','')
        product_list = PurchaseProduct.objects.filter(purchase__purchase_num=purchase_num, count__gt=F('stroage_count'))
        return render(request, 'purchase/purchase_add.html', locals())


    def post(self,request):
        user = request.user
        form = StorageAddForm(user, request.POST)
        product_split = DataSplit(eval(request.POST['purchase_product']),['product_id', 'remark', 'count', 'unit_price', 'amount'], 7, StorageProduct.objects)
        contract_operations = ContractOperations(Storage, form, sub_split1=product_split)
        contract_operations.contract_add('sales_id')
        return HttpResponse(errors[contract_operations.error_index])



class StorageModifyView(View):
    def get(self,request):
        storage_num = request.GET.get('storage_num')
        storage = Storage.objects.get(storage_num = storage_num)
        initial = {}
        for key in StorageAddForm(request).fields:
            initial[key] = getattr(storage,key)
        form = StorageAddForm(request,initial=initial)
        product_list =  PurchaseProduct.objects.filter(purchase__purchase_num=storage.purchase.purchase_num, count__gt=F('stroage_count'))
        storage_product = StorageProduct.objects.filter(storage_num=storage_num)
        return render(request, 'storage/storage_modify.html', locals())

    def post(self,request):
        form = StorageAddForm(request, request.POST)
        storage = Storage.objects.get(storage_num = request.GET.get('storage_num'))
        product_split = DataSplit(eval(request.POST['invoice_product']),['product_id', 'remark', 'count', 'unit_price', 'amount'], 7, Storage.objects)
        contract_operations = ContractOperations(Storage, form, sub_split1=product_split, )
        contract_operations.contract_modify(storage.id,'storage_id')
        return HttpResponse(errors[contract_operations.error_index])


class StorageDetailsView(View):
    def get(self,request):
        storage_num = request.GET.get('storage_num')
        storage = Storage.objects.get(storage_num = storage_num)
        initial = {}
        for key in StorageAddForm(request).fields:
            initial[key] = getattr(storage,key)
        form = StorageAddForm(request,initial=initial)
        storage_product = StorageProduct.objects.filter(storage_num=storage_num)
        return render(request, 'storage/storage_details.html', locals())



