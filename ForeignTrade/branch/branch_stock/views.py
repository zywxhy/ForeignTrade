from django.shortcuts import render,HttpResponse
from django.views import View
from .functions import StockHandle
from branch_warehousing.models import BranchWarehousing
from domestic_invoice.models import DomesticInvoiceProduct
from .serializer import BranchStockProductsModelSerializer
from branch_sales.models import BranchSalesProduct
from overseas_invoice.models import OverseasInvoice
from .models import BranchStockProducts
from datetime import date
import json
# Create your views here.
#
class BranchStockView(View):
    def get(self,request):
        stock_id = request.GET.get('stock_id','')
        data = []
        if stock_id:
            data = BranchStockProductsModelSerializer(instance=BranchStockProducts.objects.all(),many=True).data
            for item in data:
                product = item.pop('product')
                item.update(product)
        data = json.dumps(data)
        return render(request,'branch_stock/stock_products.html',locals())










# 入库审批
class WarehousingReview(View):

    def post(self,request):
        result = request.POST.get('result')
        warehousing_num = request.POST.get('warehousing_num')
        branch_warehousing = BranchWarehousing.objects.get(warehousing_num=warehousing_num)
        warehousing_product = branch_warehousing.warehousing_product.all()
        stock = branch_warehousing.branch_stock
        if branch_warehousing.status != 0:
            return HttpResponse('已审核，请勿重复审核')
        if result == 'Y':
            for product in warehousing_product:
                stock_instance = BranchStockProducts.objects.filter(stock=stock,product=product.product)
                if stock_instance:
                    stock_instance = stock_instance[0]
                    old_unit_cost = stock_instance.unit_cost
                    old_count = product.count
                    unit_cost = product.total_cost_price
                    count = product.count
                    new_cost_price = (unit_cost * count + old_count * old_unit_cost) / (count + old_count)
                    stock_instance.count += count
                    stock_instance.recent_date = date.today()
                    stock_instance.unit_cost = new_cost_price
                    stock_instance.save()
                else:
                    stock_instance.create(unit_cost=product.total_cost_price,count=product.count,recent_date=date.today(),product=product.product,
                                          stock_id=branch_warehousing.branch_stock_id)
                domestic_invoice_product = DomesticInvoiceProduct.objects.get(domestic_invoice__branchwarehousing=branch_warehousing,
                                                                              product_id=product.product.id)
                domestic_invoice_product.warehousing_count += product.count
                domestic_invoice_product.save()
                branch_warehousing.status = 1
                branch_warehousing.save()
            return HttpResponse('success')

        else:
            return HttpResponse('fail')




#出库审批
class InvoiceReview(View):
    def post(self, request):
        result = request.POST.get('result')
        invoice_num = request.POST.get('invoice_num')
        overseas_invoice = OverseasInvoice.objects.get(overseas_invoice_num=invoice_num)
        invoice_product = overseas_invoice.overseas_invoice_product.all()
        stock = overseas_invoice.branch_stock
        if result == 'Y':
            for product in invoice_product:                 # 检查
                stock_instance = BranchStockProducts.objects.filter(stock=stock,product=product.product)
                if stock_instance:
                    stock_instance = stock_instance[0]
                    if stock_instance.count < product.count:
                        return HttpResponse('{} 数量为{},需求数量为{}'.format(product.product.model,stock_instance.count,product.count))
                else:
                    stock_count = 0
                    return HttpResponse('{} 数量为0'.format(product.product.model))

            for product in invoice_product:
                stock_instance = BranchStockProducts.objects.get(stock=stock, product=product.product)
                stock_instance.count -= product.count
                # 插入记录
                stock_instance.save()

            return HttpResponse('出库成功')
        else:
            return HttpResponse('fail')

