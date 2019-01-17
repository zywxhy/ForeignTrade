import xadmin
from product.models import ProductType,Product
from .models import DomesticInvoice,DomesticInvoiceProduct

class DomesticInvoiceProductInline:
    model = DomesticInvoiceProduct
    extra = 0




class DomesticInvoiceAdmin(object):
    #model_icon = 'fa fa-tags'
    list_display = ['company','domestic_invoice_num','invoice_date','estimated_date','method','freight','address','bill','arrival_date',
                    'clearance_date','share_cost','remark',]

    #search_fields = ['type_name', 'type_id', 'type_pid', 'is_parent']
    #list_filter = ['type_name', 'type_id', 'type_pid', 'is_parent']
    #ordering = ['type_pid']
    inlines = [DomesticInvoiceProductInline,]

# class DomesticInvoiceProductAdmin(object):
#     #model_icon = 'fa fa-product-hunt'
#     list_display = '__all__'
#     # search_fields = ['product_id','name','spec','model', 'cost']
#     # list_filter = ['type','product_id','name','spec', 'cost']
#     # ordering = ['type']


xadmin.site.register(DomesticInvoice,DomesticInvoiceAdmin)
# xadmin.site.register(DomesticInvoiceProduct,DomesticInvoiceProductAdmin)