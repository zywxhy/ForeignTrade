from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView,Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from .serializer import DomesticInvoiceModelSerializer,DomesticInvoiceProductModelSerializer
from .models import DomesticInvoice,DomesticInvoiceProduct
from .forms import DomesticInvoiceModelForm
from rest_framework.routers import SimpleRouter
from .models import DomesticInvoice,DomesticInvoiceProduct
import json
from rest_framework.parsers import JSONParser
import io

# Create your views here.














class DomesticInvoiceView(View):
    def get(self,request):
        initial = None
        products_data = []
        odd_id = request.GET.get('id')
        if odd_id:
            domestic_invoice = DomesticInvoice.objects.get(pk=odd_id)
            initial = {}
            for key in DomesticInvoiceModelForm().fields:
                initial[key] = getattr(domestic_invoice, key)
            invoice_products = domestic_invoice.domestic_invoice_product
            products_data = DomesticInvoiceProductModelSerializer(instance=invoice_products, many=True, ).data
            # for item in products_data:
            #     product = item.pop('product')
            #     item.update(product)
            products_data = json.dumps(products_data)
        print(initial)
        form = DomesticInvoiceModelForm(initial=initial)  # 初始化表单，数据是表单数据
        return render(request,'domestic_invoice/domestic_invoice.html',{'form':form,'products_data':products_data})


class DomesticInvoiceListView(View):
    def get(self,request):
        domestic_invoice = DomesticInvoice.objects.all()
        return render(request,'domestic_invoice/domestic_invoice_list.html',locals())



class DomesticInvoiceViewSet(ModelViewSet):
    serializer_class = DomesticInvoiceModelSerializer
    queryset = DomesticInvoice.objects.all()
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
        serializer = self.get_serializer(data = data)
        result = serializer.is_valid()
        if not result:
            print(serializer.errors)
            return Response({'result':'failure','msg':serializer.errors})
        product_data = data.get('domestic_invoice_product','')
        if not product_data:
            return Response({'result':'failure','msg':'ERROR:No products'})
        domestic_invoice = serializer.save()
        for product in product_data:
            try:
                product.pop('domestic_invoice')
            except:
                pass
            id = product['product']['id']
            product_serializer = DomesticInvoiceProductModelSerializer(data=product,)
            product_serializer.is_valid()
            errors = product_serializer.errors
            errors.pop('domestic_invoice')
            if bool(errors):
                domestic_invoice.domestic_invoice_product.all().delete()
                print(product_serializer.errors)
                return Response({'result':'failure','msg':product_serializer.errors})
            product_serializer.save(domestic_invoice = domestic_invoice,product_id =id)
        return Response({'result':'success','msg':'success'})

router = SimpleRouter()
router.register('domestic_invoice',DomesticInvoiceViewSet)









# 海外清关
class CustomsClearance(View):
    def get(self,request):
        pass

    def post(self,request):
        pass


