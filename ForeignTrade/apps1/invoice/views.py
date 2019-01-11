from django.shortcuts import render,HttpResponse
from django.views import View
from sales.models import SalesProduct,SalesContract
from invoice.models import Invoice,InvoiceProduct
from product.models import Product
from invoice.forms import InvoiceAddForm
from django.db.models import F
from django.core import serializers
from itertools import chain
from ForeignTrade.my_class import DataSplit,ContractOperations,Layui
import json
# Create your views here.
errors = {
     0:'添加成功',
     1:'合同重复',
     2:'合同填写错误',
     3:'产品添加错误',

}

# class InvoiceView(View):
#     def get(self,request):


class InvoiceView(View):
    def get(self,request):
        user = request.user
        if user.has_perm('sales.can_read_all_sales'):
            invoice = Invoice.objects.all().order_by('invoice_date')
        else:
            invoice = Invoice.objects.filter(sales__salesman_id= user.id).order_by('invoice_date')
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
        return render(request,'invoice/invoice_view.html',locals())



class InvoiceAddView(View):
    def get(self,request):
        form = InvoiceAddForm(request,'get')
        sales_num = request.GET.get('sales_num','')
        try:
            sales_id = SalesContract.objects.get(sales_num =sales_num).id
        except:
            sales_id = 9999999
        product_list = SalesProduct.objects.filter(sales_id = sales_id,count__gt=F('outbound_count'))
        fields = ['product__model','product__name','product__spec','product__product_id','remark','outbound_count','count']
        layui = Layui(request,product_list,fields,len(product_list),)
        return render(request, 'invoice/invoice_add.html', locals())

    def post(self,request):
        form = InvoiceAddForm(request,'post',request.POST)
        sales = SalesContract.objects.get(sales_num = request.POST.get('sales_num'))
        product_split = DataSplit(request.POST['invoice_product'],['product_id', 'remark', 'count','unit_price'], InvoiceProduct)
        contract_operations = ContractOperations(Invoice, form, sub_split1=product_split,)
        contract_operations.contract_add('invoice_id',{'sales_id':sales.id},['sales_num'])
        if contract_operations.error_index == 0:
            sales.invoice_index += 1
            sales.save()
        return HttpResponse(errors[contract_operations.error_index])





class InvoiceModifyView(View):
    def get(self,request):
        invoice_num = request.GET.get('invoice_num')
        invoice = Invoice.objects.get(invoice_num=invoice_num)
        initial = {}
        for key in InvoiceAddForm(request,'get').fields:
            initial[key] = getattr(invoice,key)
        form = InvoiceAddForm(request,'get',initial=initial)
        product_list = SalesProduct.objects.filter(sales_num=invoice.sales.sales_num, count__gt=F('outbound_count'))
        invoice_product = InvoiceProduct.objects.filter(invoice_num=invoice_num)
        return render(request, 'invoice/invoice_modify.html', locals())

    def post(self,request):
        form = InvoiceAddForm(request, request.POST)
        invoice = Invoice.objects.get(invoice_num=request.GET.get('invoice_num'))
        product_split = DataSplit(request.POST['invoice_num'],['product_id', 'remark', 'count', 'unit_price', 'amount'], InvoiceProduct)
        contract_operations = ContractOperations(Invoice, form, sub_split1=product_split)
        contract_operations.contract_modify(invoice.id,'invoice_id')

        return HttpResponse(errors[contract_operations.error_index])


class InvoiceDetailsView(View):
    def get(self, request):
        invoice_num = request.GET.get('invoice_num')
        invoice = Invoice.objects.get(invoice_num=invoice_num)
        initial = {}
        for key in InvoiceAddForm(request,'add').fields:
            try:
                initial[key] = getattr(invoice, key)
            except:
                initial['sales_num'] = invoice.sales.sales_num
        form = InvoiceAddForm(request, 'add',initial=initial)
        invoice_product = InvoiceProduct.objects.filter(invoice__invoice_num=invoice_num)
        return render(request, 'invoice/invoice_details.html', locals())

    def post(self, request):
        pass


def get_sales_product(request):
    sales_num = request.GET.get('sales_num')
    sales = SalesContract.objects.get(sales_num =sales_num)
    product_list = SalesProduct.objects.filter(sales_num=sales_num)
    try:
        data = serializers.serialize('json', product_list)
        data = json.loads(data)
    except:
        data = []
    products = []
    for item in data:
        a = {}
        p = Product.objects.get(id=item['fields'].get('product'))
        for key2, value2 in p.__dict__.items():
            a[key2] = value2
        for key, value in item['fields'].items():
            a[key] = value
        a.pop('_state')
        a.pop('image')
        a.pop('cost')
        products.append(a)
        print(a)
    return HttpResponse(products,content_type='application/json')
