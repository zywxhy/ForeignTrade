from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import SimpleRouter
from rest_framework.views import Response
from .models import OverseasInvoice,OverseasInvoiceProduct
from .serializer import OverseasInvoiceModelSerializer,OverseasInvoiceProductModelSerializer
from .forms import OverseasInvoicePlanForm
from branch_sales.models import BranchSalesContract
from django.views import View
import json

# Create your views here.
class OverseasInvoiceView(View):
    def get(self,request):
        form = OverseasInvoicePlanForm(request)
        invoice_products = []
        odd_id = request.GET.get('id','')
        if odd_id:
            overseas_invoice = OverseasInvoice.objects.get(pk=odd_id)
            initial = {}
            for key,value in form.fields:
                initial[key] = getattr(overseas_invoice, key)
            form = OverseasInvoicePlanForm(request,initial=initial)
        branch_sales_id = request.GET.get('branch_sales')

        sales_products = BranchSalesContract.objects.get(id= branch_sales_id).branch_sales_product.all()
        products_data = OverseasInvoiceProductModelSerializer(instance=invoice_products, many=True, ).data
        for item in products_data:
            product = item.pop('product')
            item.update(product)
        invoice_products_data = json.dumps(products_data)
        return render(request,'overseas_invoice/overseas_invoice.html',locals())



class OverseasInvoiceViewReview(View):
    def get(self,request):
        form = OverseasInvoicePlanForm(request)
        invoice_products = []
        odd_id = request.GET.get('id','')
        if odd_id:
            overseas_invoice = OverseasInvoice.objects.get(pk=odd_id)
            initial = {}
            for key,value in form.fields:
                initial[key] = getattr(overseas_invoice, key)
            form = OverseasInvoicePlanForm(request,initial=initial)
        branch_sales_id = request.GET.get('branch_sales')

        sales_products = BranchSalesContract.objects.get(id= branch_sales_id).branch_sales_product.all()
        products_data = OverseasInvoiceProductModelSerializer(instance=invoice_products, many=True, ).data
        for item in products_data:
            product = item.pop('product')
            item.update(product)
        invoice_products_data = json.dumps(products_data)
        return render(request,'overseas_invoice/overseas_invoice.html',locals())


class OverseasInvoiceListView(View):
    def get(self,request):
        overseas_invoice = OverseasInvoice.objects.all()
        return render(request,'overseas_invoice/overseas_invoice_list.html',locals())





class OverseasInvoiceModelViewSet(ModelViewSet):
    queryset = OverseasInvoice.objects.all()
    serializer_class = OverseasInvoiceModelSerializer
    pagination_class = None

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
        overseas_invoice_product = data['overseas_invoice_product']
        for product in overseas_invoice_product:
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
        overseas_invoice_product = data.pop('overseas_invoice_product')
        sales_num = data.pop('branch_sales')
        branch_sales_id = BranchSalesContract.objects.get(sales_num=sales_num).id
        overseas_invoice_num = data['overseas_invoice_num']
        existed = OverseasInvoice.objects.filter(overseas_invoice_num=overseas_invoice_num)
        if existed:
            existed.update(branch_sales_id=branch_sales_id,**data)
            overseas_invoice = existed[0]
            overseas_invoice.overseas_invoice_product.all().delete()
        else:
            overseas_invoice = OverseasInvoice.objects.create(branch_sales_id=branch_sales_id,**data)
        for product_item in overseas_invoice_product:
            print(product_item)
            product_data = {
                'product_id':product_item.get('[id]'),
                'count':product_item.get('[count]'),

            }
            print(product_data)
            OverseasInvoiceProduct.objects.create(overseas_invoice=overseas_invoice,**product_data)
        return Response('success')







router = SimpleRouter()
router.register('overseas_invoice',OverseasInvoiceModelViewSet)