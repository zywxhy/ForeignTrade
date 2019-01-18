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
            warehousing_products_data = BranchWarehousingProductModelSerializer(instance=branch_warehousing.warehousing_product.all(), many=True).data
        else:
            domestic_invoice_id = request.GET.get('domestic_invoice', '')
            invoice_products = DomesticInvoice.objects.get(id=domestic_invoice_id).domestic_invoice_product.all()
        products_data = DomesticInvoiceProductModelSerializer(instance=invoice_products, many=True, ).data
        for item in products_data:
            invoice_count = item.pop('count')
            item.update({'invoice_count':invoice_count})
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
        product_data = data.get('domestic_invoice_product', '')
        if not product_data:         # 判断有无产品表
            return Response({'result': 'failure', 'msg': 'ERROR:No products'})
        if not result:               # 判断验证器结果，若为False，返回错误信息
            return Response({'result':'failure','msg':serializer.errors})
        branch_warehousing = serializer.save()
        if not branch_warehousing:   # 审核判断，若已审核，返回错误信息
            return Response({'result':'failure','msg':'Has been audited and no modification is allowed.'})
        for product in product_data:
            try:
                product.pop('warehousing')
            except:
                pass
            product_serializer = BranchWarehousingProductModelSerializer(data=product, )
            product_serializer.is_valid()
            errors = product_serializer.errors
            errors.pop('domestic_invoice')
            if bool(errors):
                branch_warehousing.warehousing_product.all().delete()
                print(product_serializer.errors)
                return Response({'result': 'failure', 'msg': errors})
            id = product['product']['id']
            product_serializer.save(branch_warehousing=branch_warehousing, product_id=id)

        return Response('success')


router = SimpleRouter()
router.register('branch_warehousing',BranchWarehousingViewSet)

