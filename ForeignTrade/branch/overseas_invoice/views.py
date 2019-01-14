from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import SimpleRouter
from rest_framework.views import Response
from .models import OverseasInvoice,OverseasInvoiceProduct
from .serializer import OverseasInvoiceModelSerializer,OverseasInvoiceProductModelSerializer
from .forms import OverseasInvoicePlanForm
from django.views import View
import json

# Create your views here.
class OverseasInvoiceView(View):
    def get(self,request):
        form = OverseasInvoicePlanForm(request)
        warehousing_products = []
        odd_id = request.GET.get('id','')
        if odd_id:
            overseas_invoice = OverseasInvoice.objects.get(pk=odd_id)
            initial = {}
            for key,value in form.fields:
                initial[key] = getattr(overseas_invoice, key)
            form = OverseasInvoicePlanForm(request,initial=initial)
        domestic_invoice_id = request.GET.get('domestic_invoice')

        invoice_products = OverseasInvoice.objects.get(id= domestic_invoice_id).domestic_invoice_product.all()
        products_data = OverseasInvoiceProductModelSerializer(instance=invoice_products, many=True, ).data
        for item in products_data:
            product = item.pop('product')
            item.update(product)
        invoice_products_data = json.dumps(products_data)
        return render(request,'branch_warehousing/branch_warehousing.html',locals())







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
        branch_sales_id = data.pop('branch_sales')
        overseas_invoice_num = data['overseas_invoice_num']
        existed = OverseasInvoice.objects.filter(overseas_invoice_num=overseas_invoice_num)
        if existed:
            existed.update(branch_sales_id=branch_sales_id,**data)
            domestic_invoice = existed[0]
            domestic_invoice.domestic_invoice_product.all().delete()
        else:
            domestic_invoice = OverseasInvoice.objects.create(branch_sales_id=branch_sales_id,**data)
        for product_item in overseas_invoice_product:
            print(product_item)
            product_data = {
                'product_id':product_item.get('[id]'),
                'count':product_item.get('[count]'),
                'unit_price':product_item.get('[unit_price]'),
                'remark':product_item.get('[remark]',''),
            }
            OverseasInvoiceProduct.objects.create(domestic_invoice=domestic_invoice,**product_data)
        return Response('success')







router = SimpleRouter()
router.register('overseas_invoice/api',OverseasInvoiceModelViewSet)