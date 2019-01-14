from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.views import View
from .serializer import BranchSalesContractModelSerializer,BranchSalesProductModelSerializer
from .models import BranchSalesContract,BranchSalesProduct
from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView,Response
from .forms import BranchSalesForm
import json
from branch_client.models import BranchClient
# Create your views here.

class SalesContractView(View):
    def get(self,request):
        user = request.user
        sales_num = request.GET.get('sales_num', '')
        initial = None
        products_data = []
        if sales_num:
            sales_contract = BranchSalesContract.objects.get(sales_num=sales_num, )
            initial = {}
            for key in BranchSalesForm(request.user).fields:
                initial[key] = getattr(sales_contract, key)
            sales_products = BranchSalesProduct.objects.filter(sales_num=sales_num)
            products_data = BranchSalesProductModelSerializer(instance=sales_products,many=True,).data
            print(products_data)
        form = BranchSalesForm(request.user, initial=initial)  # 初始化表单，数据是表单数据
        return render(request,'branch_sales/branch_sales.html',{'form':form,'products_data':products_data})



class SalesContractListView(View):
    def get(self,request):
        branch_sales = BranchSalesContract.objects.all()
        return render(request,'branch_sales/branch_sales_list.html',locals())



class SalesContractModelViewSet(ModelViewSet):

    serializer_class = BranchSalesContractModelSerializer
    pagination_class = None
    queryset = BranchSalesContract.objects.all()




    # def list(self, request, *args, **kwargs):jp
    #     queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         data = []
    #         for item in page:
    #             data.append(self.get_serializer(instance=item).data)
    #         return self.get_paginated_response(data)
    #     data = self.get_serializer(instance=queryset,many=True).data
    #     domestic_invoice_product = data['domestic_invoice_product']
    #     for product in domestic_invoice_product:
    #         product_info = product.pop('product')
    #         product.update(product_info)
    #     return Response(data)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'status': 0,
            'code': 0,
            'data': serializer.data,
        }
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        domestic_invoice_product = data['domestic_invoice_product']
        for product in domestic_invoice_product:
            product_info = product.pop('product')
            product.update(product_info)
        data = {
            'status': 0,
            'code': 0,
            'data': serializer.data,
        }
        return Response(data)

    # 产品的添加和修改
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        branch_sales_product = request.data.get('branch_sales_product')
        branch_sales_product = json.loads(branch_sales_product)
        serializer.is_valid()
        data = serializer.data  # 这里嵌套的product信息会自动在key值上加[]，如：'id' 变成 '[id]' 后续处理要注意
        print(data)
        client_id = data.pop('client')
        sales_num = data['sales_num']
        existed = BranchSalesContract.objects.filter(sales_num=sales_num)
        if existed:
            existed.update(client_id=client_id, **data)
            branch_sales = existed[0]
            branch_sales.branch_sales_product.all().delete()
        else:
            branch_sales = BranchSalesContract.objects.create(client_id=client_id, **data)
        for product_item in branch_sales_product:
            print(product_item)
            product_data = {
                'product_id': product_item.get('id'),
                'sales_count': product_item.get('sales_count'),
                'unit_price': product_item.get('unit_price'),
                'remark': product_item.get('remark', ''),
            }
            BranchSalesProduct.objects.create(branch_sales=branch_sales, **product_data)
        return Response('success')



router = SimpleRouter()
router.register('branch_sales',SalesContractModelViewSet)