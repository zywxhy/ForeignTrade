import xadmin
from product.models import ProductType,Product
from .models import BranchStock,BranchStockProducts,BranchStockRecord






class BranchStockAdmin(object):
    #model_icon = 'fa fa-tags'
    list_display = ['company','name',]

    #search_fields = ['type_name', 'type_id', 'type_pid', 'is_parent']
    #list_filter = ['type_name', 'type_id', 'type_pid', 'is_parent']
    #ordering = ['type_pid']




xadmin.site.register(BranchStock,BranchStockAdmin)
