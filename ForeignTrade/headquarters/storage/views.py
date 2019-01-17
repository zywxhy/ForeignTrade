from django.shortcuts import render,HttpResponse,get_object_or_404
from django.views import View
from storage.forms import StorageAddForm
from storage.models import Storage,StorageProduct
from purchase.models import PurchaseProduct,PurchaseContract
from stock.models import StockProduct,StockRecord
from django.db.models import F
from itertools import chain
import json
from ForeignTrade.my_class import DataSplit,ContractOperations,Layui
# Create your views here.

errors = {
     0:'添加成功',
     1:'合同重复',
     2:'合同填写错误',
     3:'产品添加错误',

}

class StorageView(View):
    pass



# 入库计划单添加
class StorageAddView(View):
    def get(self,request):
        user = request.user
        form = StorageAddForm(request,'get')
        purchase_num = request.GET.get('purchase_num','')
        purchase = get_object_or_404(PurchaseContract,**{'purchase_num' :purchase_num})
        purchase_id = purchase.id
        product_list = PurchaseProduct.objects.filter(purchase_id=purchase_id, purchase_count__gt=F('storage_count'))
        products = PurchaseProduct.sales_serializers(product_list)
        return render(request, 'storage/storage_add.html', locals())

    def post(self,request):
        form = StorageAddForm(request,'post',request.POST)
        purchase_num = request.POST.get('purchase_num','')
        print(purchase_num)
        purchase = PurchaseContract.objects.get(purchase_num=purchase_num)
        product_split = DataSplit(request.POST['storage_product'],['product_id', 'remark', 'count', ], StorageProduct)
        contract_operations = ContractOperations(Storage, form, sub_split1=product_split)
        contract_operations.contract_add('storage_id',{'purchase_id':purchase.id},['purchase_num'])
        return HttpResponse(errors[contract_operations.error_index])



# 入库计划单修改
class StorageModifyView(View):
    def get(self,request):
        storage_num = request.GET.get('storage_num')
        storage = Storage.objects.get(storage_num = storage_num)
        initial = {}
        for key in StorageAddForm(request,'get').fields:
            initial[key] = getattr(storage,key)
        form = StorageAddForm(request,'get',initial=initial,)
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


#入库计划单详情页
class StorageDetailsView(View):
    def get(self,request):
        storage_num = request.GET.get('storage_num')
        storage = Storage.objects.get(storage_num = storage_num)
        initial = {}
        for key in StorageAddForm(request,'get').fields:
            initial[key] = getattr(storage,key)
        form = StorageAddForm(request,'get',initial=initial)
        storage_product = StorageProduct.objects.filter(storage_num=storage_num)
        return render(request, 'storage/storage_details.html', locals())




class ActualStorageView(View):
    def get(self,request):
        storage_num = request.GET.get('storage_num')
        storage = Storage.objects.get(storage_num=storage_num)
        initial = {}
        for key in StorageAddForm(request,'get').fields:
            initial[key] = getattr(storage, key)
        form = StorageAddForm(request, 'get',initial=initial,)
        storage_product = StorageProduct.objects.filter(storage_num=storage_num)
        return render(request, 'storage/storage_details.html', locals())

    def post(self,request):
        try:
            storage_num = request.POST['storage_num']
            stock_id = request.POST['stock_id']
        except:
            return HttpResponse('the storage or the stock is not exist')
        storage = Storage.objects.get(storage_num=storage_num)
        storage_product = storage.storageproduct_set.all()
        product_data = json.loads(request.POST.get('storage_product'))
        for item in product_data:
            product = storage_product.get(storage__storage_num=storage_num,product__product_id=item['product__product_id'])
            product.count += item.count
            product.save()
            stock_product = StockProduct.objects.get(stock_id = stock_id,product__product_id=item['product__product_id'])

        return HttpResponse('')


