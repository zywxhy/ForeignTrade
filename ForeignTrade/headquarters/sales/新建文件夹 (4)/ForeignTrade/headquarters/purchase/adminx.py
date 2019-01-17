import xadmin
from purchase.models import PurchaseContract,PurchaseProduct


class PurchaseProductInline(object):
    model = PurchaseProduct
    extra = 0


class PurchaseAdmin(object):
    # model_icon = 'fa fa-buysellads'

    list_display = ['purchase_num', 'sales_num', 'buyer','date', 'supplier', 'total_amount','status']
    search_field = ['purchase_num', 'buyer', ]
    list_filter = ['buyer', 'supplier', 'status','date']

    inlines = [PurchaseProductInline, ]



xadmin.site.register(PurchaseContract, PurchaseAdmin)