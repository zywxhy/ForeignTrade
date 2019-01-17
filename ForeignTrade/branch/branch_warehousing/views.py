from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.views import View
from rest_framework.views import Response
from rest_framework.routers import SimpleRouter
from .serializer import BranchWarehousingModelSerializer
from .models import BranchWarehousing,BranchWarehousingProduct
from domestic_invoice.serializer import DomesticInvoiceProductModelSerializer
from domestic_invoice.models import DomesticInvoice
from .forms import BranchWarehousingModelForm
from .serializer import BranchWarehousingProductModelSerializer
import json
# Create your views here.

class BranchWarehousingView(View):
    def get(self,request):
        form = BranchWarehousingModelForm(request)
        warehousing_products_data = []
        odd_id = request.GET.get('id','')

        if odd_id:
            branch_warehousing = BranchWarehousing.objects.get(pk=odd_id)
            invoice_products = branch_warehousing.domestic_invoice.domestic_invoice_product.all()
            initial = {}
            for key in form.fields:
                initial[key] = getattr(branch_warehousing, key)
            form = BranchWarehousingModelForm(request,initial=initial)
            warehousing_products_data = BranchWarehousingProductModelSerializer(
                instance=branch_warehousing.warehousing_product.all(), many=True).data
            for item in warehousing_products_data:
                product = item.pop('product')
                item.update(product)
        else:
            domestic_invoice_id = request.GET.get('domestic_invoice', '')
            invoice_products = DomesticInvoice.objects.get(id=domestic_invoice_id).domestic_invoice_product.all()
        products_data = DomesticInvoiceProductModelSerializer(instance=invoice_products, many=True, ).data
        for item in products_data:
            product = item.pop('product')
            item.update(product)
        invoice_products_data = json.dumps(products_data)
        warehousing_products_data = json.dumps(warehousing_products_data)
        return render(request,'branch_warehousing/branch_warehousing.html',locals())


class BranchWarehousingReviewView(View):
    def get(self,request):
        form = BranchWarehousingModelForm(request)
        warehousing_products = []
        odd_id = request.GET.get('id','')
        warehousing_products_data = []
        if odd_id:
            branch_warehousing = BranchWarehousing.objects.get(pk=odd_id)
            initial = {}
            for key in form.fields:
                initial[key] = getattr(branch_warehousing, key)
            form = BranchWarehousingModelForm(request,initial=initial)
            warehousing_products_data = BranchWarehousingProductModelSerializer(instance=branch_warehousing.warehousing_product.all(),many=True).data
            for item in warehousing_products_data:
                product = item.pop('product')
                item.update(product)
        warehousing_products_data = json.dumps(warehousing_products_data)




        return render(request,'branch_stock/branch_stock_warehousing.html',locals())



class BranchWarehousingListView(View):
    def get(self,request):
       branch_warehousing = BranchWarehousing.objects.all()
       return render(request,'branch_warehousing/branch_warehousing_list.html',locals())



class BranchWarehousingViewSet(ModelViewSet):
    serializer_class = BranchWarehousingModelSerializer
    queryset = BranchWarehousing.objects.all()

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
        warehousing_product = data['warehousing_product']
        for product in warehousing_product:
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
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid()
        data = serializer.data    # 这里嵌套的product信息会自动在key值上加[]，如：'id' 变成 '[id]' 后续处理要注意
        branch_stock_id = data.pop('branch_stock')
        warehousing_product = data.pop('warehousing_product')
        domestic_invoice_num = data.pop('domestic_invoice')
        domestic_invoice = DomesticInvoice.objects.get(domestic_invoice_num=domestic_invoice_num)
        warehousing_num = data['warehousing_num']
        existed = BranchWarehousing.objects.filter(warehousing_num=warehousing_num)
        if existed:
            existed.update(branch_stock_id=branch_stock_id,domestic_invoice=domestic_invoice,**data)
            warehousing = existed[0]
            warehousing.warehousing_product.all().delete()
        else:
            warehousing = BranchWarehousing.objects.create(branch_stock_id=branch_stock_id,domestic_invoice=domestic_invoice,**data)
        for product_item in warehousing_product:
            print(product_item)
            product_data = {
                'product_id':product_item.get('[id]'),
                'count':product_item.get('[count]'),
               # 'unit_price':product_item.get('[unit_price]'),
                'remark':product_item.get('[remark]',''),
            }
            BranchWarehousingProduct.objects.create(warehousing=warehousing,**product_data)
        return Response('success')


router = SimpleRouter()
router.register('branch_warehousing',BranchWarehousingViewSet)

