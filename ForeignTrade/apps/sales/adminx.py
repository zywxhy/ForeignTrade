import xadmin

from sales.models import SalesContract,SalesProduct,CollectionPlan


class SalesProductInline:
    model = SalesProduct
    extra = 0

class CollectionPlanInline:
    model = CollectionPlan
    extra = 0


class SalesContractAdmin:
    model_icon = 'fa fa-buysellads'

    list_display = ['sales_num','salesman','date','client','total_amount','status']
    search_field = ['sales_num','salesman','date','client']
    list_filter = ['salesman','date','client','status']
    exclude = ['invoice_index','refund_index']
    inlines = [SalesProductInline,CollectionPlanInline]

class SalesProductAdmin:
    model_icon = 'fa fa-shopping-basket'

    list_display = ['sales','product', 'remark', 'count', 'outbound_count', 'return_count', 'unit_price']
    search_field = ['product', 'sales']
    list_filter = ['product', 'sales','count']
    exclude = ['status']


class CollectionPlanAdmin:
    model_icon = 'fa fa-dollar'

    list_display = ['sales', 'receipt_type', 'receipt', 'receipt_time']
    search_field = ['sales']
    list_filter = ['sales']


xadmin.site.register(SalesContract,SalesContractAdmin)
#xadmin.site.register(SalesProduct,SalesProductAdmin)
#xadmin.site.register(CollectionPlan,CollectionPlanAdmin)
