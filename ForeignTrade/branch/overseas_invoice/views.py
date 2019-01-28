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
from branch_sales.serializer import BranchSalesProductModelSerializer
from django.db.models import Q,F

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
        sales_products_data = json.dumps(BranchSalesProductModelSerializer(instance=sales_products,many=True).data)
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

        sales_products = BranchSalesContract.objects.get(id= branch_sales_id).branch_sales_product.filter()
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
        data = json.loads(request.data.get('data'))
        print(data)
        serializer = self.get_serializer(data=data)
        result = serializer.is_valid()
        if not result:
            print(serializer.errors)
            return Response({'result': 'failure', 'msg': serializer.errors})
        product_data = data.get('domestic_invoice_product', '')
        if not product_data:
            return Response({'result': 'failure', 'msg': 'ERROR:No products'})
        domestic_invoice = serializer.save()
        if not domestic_invoice:
            return Response({'result': 'failure', 'msg': 'Has been audited and no modification is allowed.'})
        for product in product_data:
            try:
                product.pop('domestic_invoice')
            except:
                pass
            id = product['product']['id']
            product_serializer = OverseasInvoiceProductModelSerializer(data=product, )
            product_serializer.is_valid()
            errors = product_serializer.errors
            errors.pop('domestic_invoice')
            if bool(errors):
                domestic_invoice.domestic_invoice_product.all().delete()
                print(product_serializer.errors)
                return Response({'result': 'failure', 'msg': product_serializer.errors})
            product_serializer.save(domestic_invoice=domestic_invoice, product_id=id)
        return Response({'result': 'success', 'msg': 'success'})


router = SimpleRouter()
router.register('overseas_invoice',OverseasInvoiceModelViewSet)