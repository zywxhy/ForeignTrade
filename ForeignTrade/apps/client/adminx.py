import xadmin
from client.models import Client




class ClientAdmin(object):
    model_icon = 'fa fa-area'
    list_display = ['company_name','name','area','salesman','info','area','level','credit']
    search_fields = ['salesman','area']
    list_filter = ['salesman','area','recent_date']



xadmin.site.register(Client,ClientAdmin)