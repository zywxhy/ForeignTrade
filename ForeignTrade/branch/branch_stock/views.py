from django.shortcuts import render
from django.views import View
from .functions import StockHandle
from branch_warehousing.models import BranchWarehousing
from overseas_invoice.models import OverseasInvoice
from .models import BranchStockProducts
# Create your views here.
#

# 入库审批
def warehousing_review(View):
    def post(request):
        result = request.POST.get('Y')
        branch_warehousing_num = request.POST.get('branch_warehousing_num')
        branch_warehousing = BranchWarehousing.objects.get(branch_warehousing_num=branch_warehousing_num)
        warehousing_product = branch_warehousing.warehousing_product.all()
        if result == 'Y':
            for product in warehousing_product:
                stock_instance = BranchStockProducts.objects.get_or_create(stock_id=branch_warehousing.branch_stock_id,product_id = product.id )
                stock_handle = StockHandle(stock_instance,branch_warehousing)
