import xadmin
from product.models import ProductType,Product


class ProductTypeAdmin(object):
    model_icon = 'fa fa-tags'
    list_display = ['type_name', 'type_id', 'type_pid', 'is_parent']
    search_fields = ['type_name', 'type_id', 'type_pid', 'is_parent']
    list_filter = ['type_name', 'type_id', 'type_pid', 'is_parent']
    ordering = ['type_pid']


class ProductAdmin(object):
    model_icon = 'fa fa-product-hunt'
    list_display = ['type','product_id','name','spec','cost']
    search_fields = ['product_id','name','spec','model', 'cost']
    list_filter = ['type','product_id','name','spec', 'cost']
    ordering = ['type']


xadmin.site.register(ProductType,ProductTypeAdmin)
xadmin.site.register(Product,ProductAdmin)