from django.shortcuts import render,HttpResponse
from django.views import View
from purchase.forms import PurchaseForm
from purchase.models import PurchaseContract,PurchaseProduct,Payment
from sales.models import SalesContract,SalesProduct
from users.views import LoginRequiredMixin
from ForeignTrade.my_class import DataSplit,ContractOperations,Layui
from itertools import chain
from django.db.models import F,Q
# Create your views here.
errors = {
     0:'添加成功',
     1:'合同重复',
     2:'合同填写错误',
     3:'产品添加错误',

}





class PurchaseView(LoginRequiredMixin,View):
    def get(self,request):
        user = request.user
        if user.has_perm('purchase.can_read_all_purchase'):
            purchase_contract = PurchaseContract.objects.all().order_by('date')
        else:
            purchase_contract = PurchaseContract.objects.filter(buyer_id=user.id).order_by('date')
                # fields = ['id','sales_num',]
                # sales = []
                # for item in sales_contract:
                #     ele = {}

                #     for field in fields:
                #         ele[field] = getattr(item,field)
                #     ele['salesman'] = item.salesman.first_name
                #     ele['client']  = item.client.name
                #     ele['date'] = item.date.__str__()
                #     ele['status'] = SalesContract.sales_status[item.status][1]
                #     sales.append(ele)
                # data = json.dumps(sales)
                # del sales
        return render(request, 'purchase/purchase_view.html', locals())

    @staticmethod
    def get_sales(request):
        user = request.user
        sales_contract = SalesContract.objects.filter(Q(status=0)| Q(status=1),salesman__company__company_id='1')
        fields = ['date','salesman__first_name','sales_num']
        page = request.GET.get('page',None)
        limit = request.GET.get('limit',None)
        layui = Layui(request,sales_contract,fields,len(sales_contract),page,limit)
        json_data = layui.laytable_url()
        return HttpResponse(json_data,content_type='application/json')


class PurchaseAddView(View):
    def get(self,request):
        user = request.user
        sales_num = request.GET.get('sales_num',None)
        form = PurchaseForm(request,initial={'sales_num':sales_num})
        #sales_product_list = request.POST.get('sales_product_list').split('@*')
        try:
            sales_id = SalesContract.objects.get(sales_num =sales_num).id
        except:
            sales_id = 9999999
        print(sales_id)
        product_list = SalesProduct.objects.filter(sales_id=sales_id, sales_count__gt=F('outbound_count'))
        return render(request, 'purchase/purchase_add.html', locals())


    def post(self,request):
        form = PurchaseForm(request,request.POST)
        #product_split = DataSplit(request.POST['invoice_product'], ['product_id', 'remark', 'count', 'unit_price'],InvoiceProduct)
        #contract_operations = ContractOperations(Invoice, form, sub_split1=product_split, )
        product_split = DataSplit(request.POST.get('purchase_product'),['product_id', 'remark', 'count', 'unit_price', 'amount'], PurchaseProduct)
        purchase_payment = request.POST.get('purchase_payment', None)
        if purchase_payment is not None:
            payment_split = DataSplit(request.POST.get('purchase_payment',None),['payment_time', 'payment_type', 'payment_time', 'payment'], Payment)
        else:
            payment_split = None
        contract_operations = ContractOperations(PurchaseContract, form, sub_split1=product_split,sub_split2=payment_split)
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








