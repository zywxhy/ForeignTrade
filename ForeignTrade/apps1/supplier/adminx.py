import xadmin
from supplier.models import Supplier,SupplierContacts,SupplierProduct

class SupplierContactsInline(object):
    model = SupplierContacts
    extra = 0


class SupplierProductInline(object):
    model = SupplierProduct
    extra = 0


class SupplierAdmin(object):
    list_display = ['name','address','inputting_date','telephone']
    search_fields = ['name','address','inputting_date']
    list_filter = ['name', 'area',]

    inlines = [SupplierContactsInline,SupplierProductInline]



xadmin.site.register(Supplier,SupplierAdmin)