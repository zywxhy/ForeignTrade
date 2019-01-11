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
# Create your views here.

class DomesticInvoiceView(View):
    def get(self,request):
        form = DomesticInvoiceModelForm()
        return render(request,'domestic_invoice/domestic_invoice.html',{'form':form})



class DomesticInvoiceViewSet(ModelViewSet):
    serializer_class = DomesticInvoiceModelSerializer
    queryset = DomesticInvoice.objects.all()
    pagination_class = None

    # def list(self, request, *args, **kwargs):
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
            'data': [data],
        }
        return Response(data)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid()
        data = serializer.data
        domestic_invoice_product = data.pop('domestic_invoice_product')
        company_id = data.pop('company')
        domestic_invoice_num = data['domestic_invoice_num']
        existed = DomesticInvoice.objects.filter(domestic_invoice_num=domestic_invoice_num)
        if existed:
            existed.update(company_id=company_id,**data)
            domestic_invoice = existed[0]
            domestic_invoice.domestic_invoice_product.all().delete()
        else:
            domestic_invoice = DomesticInvoice.objects.create(company_id=company_id,**data)
        for product_item in domestic_invoice_product:
            print(product_item)
            product_data = {
                'product_id':product_item.get('[id]'),
                'count':product_item.get('[count]'),
                'unit_price':product_item.get('[unit_price]'),
                'remark':product_item.get('[remark]',''),
            }
            DomesticInvoiceProduct.objects.create(domestic_invoice=domestic_invoice,**product_data)
        return Response('success')



class DomesticInvoiceProductsViewSet(ModelViewSet):
    serializer_class = DomesticInvoiceProductModelSerializer
    queryset = DomesticInvoiceProduct.objects.all()
    pagination_class = None



router = SimpleRouter()
router.register('domestic_invoice',DomesticInvoiceViewSet)
router.register('domestic_invoice_products',DomesticInvoiceProductsViewSet)


