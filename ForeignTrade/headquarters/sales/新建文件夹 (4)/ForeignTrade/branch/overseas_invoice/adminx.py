import xadmin
from product.models import ProductType,Product
from .models import OverseasInvoice,OverseasInvoiceProduct

class OverseasInvoiceProductInline:
    model = OverseasInvoiceProduct
    extra = 0




class OverseasInvoiceAdmin(object):
    #model_icon = 'fa fa-tags'
    list_display = ['branch_sales','overseas_invoice_num','invoice_date','maker','remark','shipping_method',]

    #search_fields = ['type_name', 'type_id', 'type_pid', 'is_parent']
    #list_filter = ['type_name', 'type_id', 'type_pid', 'is_parent']
    #ordering = ['type_pid']
    inlines = [OverseasInvoiceProductInline,]

# class DomesticInvoiceProductAdmin(object):
#     #model_icon = 'fa fa-product-hunt'
#     list_display = '__all__'
#     # search_fields = ['product_id','name','spec','model', 'cost']
#     # list_filter = ['type','product_id','name','spec', 'cost']
#     # ordering = ['type']


xadmin.site.register(OverseasInvoice,OverseasInvoiceAdmin)
# xadmin.site.register(DomesticInvoiceProduct,DomesticInvoiceProductAdmin)