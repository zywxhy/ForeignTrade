import xadmin
from stock.models import Stock,StockProduct





class StockAdmin(object):
    model_icon = 'fa fa-square'

    list_display = ['company','name']
    search_fields = ['company','name']
    list_filter = ['company','name']


class StockProductAdmin(object):
    list_display = ['stock','product', 'count','unit_cost','recent_date']
    search_fields = ['product', 'unit_cost']
    list_filter = ['stock', 'product','recent_date']


xadmin.site.register(Stock,StockAdmin)
xadmin.site.register(StockProduct,StockProductAdmin)