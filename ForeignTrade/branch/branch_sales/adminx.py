import xadmin
from product.models import ProductType,Product
from .models import BranchSalesContract,BranchSalesProduct

class BranchSalesProductInline:
    model = BranchSalesProduct
    extra = 0



class BranchSalesContractAdmin(object):
    #model_icon = 'fa fa-tags'
    list_display = ['sales_num','salesman','maker','sales_date','client','currency','price_clause','status','total_amount','remark']

    #search_fields = ['type_name', 'type_id', 'type_pid', 'is_parent']
    #list_filter = ['type_name', 'type_id', 'type_pid', 'is_parent']
    #ordering = ['type_pid']
    inlines = [BranchSalesProductInline,]

# class DomesticInvoiceProductAdmin(object):
#     #model_icon = 'fa fa-product-hunt'
#     list_display = '__all__'
#     # search_fields = ['product_id','name','spec','model', 'cost']
#     # list_filter = ['type','product_id','name','spec', 'cost']
#     # ordering = ['type']


xadmin.site.register(BranchSalesContract,BranchSalesContractAdmin)
# xadmin.site.register(DomesticInvoiceProduct,DomesticInvoiceProductAdmin)