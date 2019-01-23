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
            sales_products = BranchSalesProduct.objects.filter(branch_sales=sales_contract)
            products_data = BranchSalesProductModelSerializer(instance=sales_products,many=True,).data
        products_data = json.dumps(products_data)
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
        data = {
            'status': 0,
            'code': 0,
            'data': serializer.data,
        }
        return Response(data)

    # 产品的添加和修改
    def create(self, request, *args, **kwargs):
        data = json.loads(request.data.get('data'))
        print(data)
        serializer = self.get_serializer(data=data)
        result = serializer.is_valid()
        if not result:
            print(serializer.errors)
            return Response({'result': 'failure', 'msg': serializer.errors})
        product_data = data.get('branch_sales_product', '')
        if not product_data:
            return Response({'result': 'failure', 'msg': 'ERROR:No products'})
        branch_sales = serializer.save()
        if not branch_sales:
            return Response({'result': 'failure', 'msg': 'Has been audited and no modification is allowed.'})
        for product in product_data:
            try:
                product.pop('branch_sales')
            except:
                pass
            id = product['product']['id']
            product_serializer = BranchSalesProductModelSerializer(data=product, )
            product_serializer.is_valid()
            errors = product_serializer.errors
            errors.pop('branch_sales')
            if bool(errors):
                branch_sales.branch_sales_product.all().delete()
                print(product_serializer.errors)
                return Response({'result': 'failure', 'msg': product_serializer.errors})
            product_serializer.save(branch_sales=branch_sales, product_id=id)
        return Response({'result': 'success', 'msg': 'success'})



router = SimpleRouter()
router.register('branch_sales',SalesContractModelViewSet)
