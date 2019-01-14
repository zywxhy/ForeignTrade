import xadmin
from .models import BranchClient




class BranchClientAdmin(object):
    model_icon = 'fa fa-area'
    list_display = ['company_name','name','salesman','info','address','level','credit']
    search_fields = ['salesman','address']
    list_filter = ['salesman','address','recent_date']



xadmin.site.register(BranchClient,BranchClientAdmin)