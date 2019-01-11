from django.shortcuts import render,HttpResponse
from django.views import View
from sales.models import SalesContract,SalesProduct,CollectionPlan,SalesStatistics
from users.models import MyUser,Company
from client.models import Client
from product.models import Product
from sales.forms import SalesForm,SalesModelForm
from users.views import LoginRequiredMixin
from collections import Counter
from datetime import date
import json
from collections import defaultdict
from ForeignTrade.my_class import DataSplit,ContractOperations,Layui
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.core import serializers
from django.core.paginator import Paginator
import re
# Create your views here.


errors = {
     0:'添加成功',
     1:'合同重复',
     2:'合同填写错误',
     3:'产品添加错误',
     4:'收款计划添加错误',
     5:'其他错误'

}


#销售合同添加
class SalesAddView(LoginRequiredMixin,View):

    def get(self,request):
        user = request.user
        form = SalesForm(user)
        sales_contract = SalesContract.objects.all()
        return render(request,'sales/sales_add.html',locals())

    def post(self,request):
        user = request.user
        form = SalesForm(user,request.POST)
        json.loads(request.POST.get('sales_collection',''))
        print(json.loads(request.POST['sales_product']))
        product_split = DataSplit(request.POST['sales_product'],['product_id','remark','count','unit_price','amount'],SalesProduct)
        collection_split = DataSplit(request.POST['sales_collection'],['receipt','receipt_type','receipt_time','remark'],CollectionPlan)
        contract_operations = ContractOperations(SalesContract,form,sub_split1=product_split,sub_split2=collection_split)
        contract_operations.contract_add('sales_id')
        return HttpResponse(errors[contract_operations.error_index])




#销售合同修改
class SalesContractModify(View):
    def get(self, request):
        sales_num = request.GET.get('sales_num')
        sales = SalesContract.objects.get(sales_num=sales_num)
        initial = {}
        for key in SalesForm(request.user).fields:
            initial[key] =getattr(sales,key)
        form = SalesForm(request.user,initial=initial)
        product_list = SalesProduct.objects.filter(sales_id=sales.id)
        try:
            data = serializers.serialize('json', product_list)
            data = eval(data)
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
            del a
        return render(request, 'sales/sales_modify.html', locals())

    def post(self, request):
        sales_num = request.GET.get('sales_num')
        sales = SalesContract.objects.get(sales_num=sales_num)
        form = SalesForm(request.user, request.POST)
        product_split = DataSplit(eval(request.POST['sales_product']),['product_id', 'remark', 'count', 'unit_price', 'amount'], 7, SalesProduct.objects)
        collection_split = DataSplit(eval(request.POST['sales_collection']),['receipt_type', 'receipt_time', 'receipt', 'remark'], 4, CollectionPlan.objects)
        contract_operations = ContractOperations(SalesContract, form, sub_split1=product_split,sub_split2=collection_split)
        contract_operations.contract_modify(sales.id,'sales_id')
        return HttpResponse(errors[contract_operations.error_index])



# 查看销售合同列表
class SalesContractView(LoginRequiredMixin,View):
    def get(self,request):
        user = request.user

        if user.has_perm('sales.can_read_all_sales'):
            sales_contract = SalesContract.objects.all().order_by('date')
        elif user.permission_level==3:
            sales_contract = SalesContract.objects.filter(salesman__company_id = user.company_id).order_by('date')
        else:

            sales_contract = SalesContract.objects.filter(salesman_id = user.id).order_by('date')
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
        return render(request,'sales/sales_view.html',locals())




#销售合同详细
class SalesDetailsView(LoginRequiredMixin,View):
    def get(self, request):
        user = request.user
        sales_num = request.GET.get('sales_num','')
        sales_contract = SalesContract.objects.get(sales_num=sales_num)
        initial = {}
        for key in SalesForm(request.user).fields:
            initial[key] = getattr(sales_contract,key)
        form = SalesForm(request.user,initial=initial)

        product_list = SalesProduct.objects.filter(sales_id=sales_contract.id)
        try:
            data = serializers.serialize('json', product_list)
            data = eval(data)
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
            a.pop('unit_price')
            products.append(a)
            print(a)
        form = SalesForm(request.user,initial=initial)
        return render(request, 'sales/sales_details.html', locals())


class SalesProductView(LoginRequiredMixin,View):
    def get(self,request):
        user = request.user
        company_id = request.GET.get('company_id',None)
        limit = request.GET.get('limit',10)
        page = request.GET.get('page',1)
        field = request.GET.get('field', None)
        order = request.GET.get('order', None)


        if company_id is None:
            company_id = user.company_id
        if user.permission_level > 3:
            sales_product = SalesProduct.objects.filter(sales__salesman__company_id=2)
        else:
            if user.company_id != company_id:
                return HttpResponse('No permisson')
            else:
                sales_product = SalesProduct.objects.filter(sales__salesman__company_id=company_id)

        if field is not None:

            if order == 'desc':
                sales_product = sales_product.order_by(field).reverse()
            else:
                sales_product = sales_product.order_by(field)

        count = len(sales_product)
        paginator = Paginator(sales_product,limit)
        context = paginator.page(page)
        fields = ['sales__date','sales__client__name','sales__salesman__first_name','sales__sales_num','product__model',
                    'product__name','product__spec','count']
        layui = Layui(request,context,fields,count)
        json_data = json.dumps(layui.laytable_url())
        return HttpResponse(json_data,content_type='application/json')


class SalesProdcutListView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'sales/sales_product.html',{})


class SalesStatisticsView(LoginRequiredMixin,View):
    def get(self,request):
        sales_statistics = SalesStatistics.objects.all()
        staistics = []
        for sales in sales_statistics:
            count = defaultdict(lambda:{})
            staistics[sales.client.name].__setitem__(sales.product.model+':'+sales.product.spec,{})
        for sales in sales_statistics:
            staistics[sales.client.name][sales.product.model+':'+sales.product.spec].__setitem__(str(sales.year)+'/'+str(sales.month))

        return render(request,'sales/sales_statistics.html',locals())


    def post(self,request):
        pass



        for product in SalesProduct.objects.filter(salesman__company__id=request.user.company_id):
            product_id = product.sales.date + product.product_id + product.count
            pass



class SalesStatisticsSynView(View):
    def get(self,request):
        sales_product = SalesProduct.objects.all()
        sales_statistics = SalesStatistics.objects.all()
        for product in sales_product:
            data = {}
            data['company_id'] = product.sales.salesman.company_id
            data['product_id'] = product.product_id
            data['client_id'] = product.sales.client_id
            data['year'] = product.sales.date.year
            data['month'] = product.sales.date.month
            try:                #是否有该条数据
                item = sales_statistics.get(**data)
            except Exception as e:
                print(e)
                item = sales_statistics.create(**data)
            item.count += product.count
            item.save()


    def post(self,request):
        pass




def get_sales_info(request):
    sales_num = request.GET.get('sales_num')
    products = SalesProduct.objects.filter(sales__sales_num=sales_num)
    data = SalesProduct.sales_serializers(products)
    return HttpResponse(data,content_type='application/json')


