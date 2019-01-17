import xadmin
from finance.models import ExchangeRate
from sales.models import CollectionPlan



class ExchangeRateAdmin(object):
    model_icon = 'fa fa-dollar'
    list_display = ['currency','type','date','exchange_rate']
    search_fields = ['currency','type']
    list_filter = ['currency','type','date']
    relfield_style = 'fk_ajax'





xadmin.site.register(ExchangeRate,ExchangeRateAdmin)



