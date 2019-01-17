from django.shortcuts import render
from django.views import View
#from supplier.models import Supplier

# Create your views here.


class SupplierView(View):
    def get(self,request):
        #supplier = Supplier.objects.all()
        return render(request,'supplier/supplier.html',locals())


class SupplierInfoView(View):
    def get(self,request):
        supplier_id = request.GET.get('supplier_id')
        #supplier = Supplier.objects.get(id=supplier_id)
        return render(request,'supplier/supplier_info.html',locals())



class SupplierSelectView(View):
    def get(self,request):
        #supplier = Supplier.objects.all()
        return render(request, 'supplier/supplier_select.html', locals())


