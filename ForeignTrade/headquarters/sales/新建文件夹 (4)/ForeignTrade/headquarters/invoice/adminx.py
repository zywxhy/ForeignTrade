import xadmin
from invoice.models import Invoice,InvoiceProduct

class InvoiceProductInline(object):
    model = InvoiceProduct
    extra = 0



class InvoiceAdmin(object):
    # model_icon = 'fa fa-buysellads'

    list_display = ['invoice_num', 'sales', 'maker', 'invoice_date',  'status']
    search_field = ['sales', 'maker',]
    list_filter = ['sales', 'invoice_date', 'status']

    inlines = [InvoiceProductInline,]



xadmin.site.register(Invoice,InvoiceAdmin)