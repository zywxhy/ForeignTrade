import xadmin
from storage.models import Storage,StorageProduct


class StorageProductInline(object):
    model = StorageProduct
    extra = 0


class StorageAdmin(object):
    # model_icon = 'fa fa-buysellads'

    list_display = ['storage_num', 'purchase', 'maker','reviewer', 'warehouse_date', 'deadline','status']
    search_field = ['storage_num', 'purchase', 'maker',]
    list_filter = [ 'purchase','warehouse_date','deadline','status']

    inlines = [StorageProductInline, ]



xadmin.site.register(Storage, StorageAdmin)