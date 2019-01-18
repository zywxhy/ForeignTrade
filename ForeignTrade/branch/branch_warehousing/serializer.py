from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import BranchWarehousing,BranchWarehousingProduct
from domestic_invoice.serializer import ProductModelSerializer,DomesticInvoice,Product
from rest_framework.routers import SimpleRouter
from rest_framework.serializers import ReturnDict,ReturnList

class BranchWarehousingProductModelSerializer(ModelSerializer):
    product = ProductModelSerializer(read_only=True)

    class Meta:
        model = BranchWarehousingProduct
        fields = '__all__'

    def save(self,**kwargs):
        branch_warehousing = kwargs.pop('branch_warehousing')
        product_id = kwargs.pop('product_id')
        data = self.data
        self.instance = BranchWarehousingProduct.objects.create(product_id=product_id, warehousing=branch_warehousing,**data)
        return self.instance




class BranchWarehousingModelSerializer(ModelSerializer):
    warehousing_product = BranchWarehousingProductModelSerializer(many=True,read_only=True)
    class Meta:
        model = BranchWarehousing
        fields = '__all__'


    def save(self, **kwargs):
        data = self.data
        branch_stock_id = data.pop('branch_stock')
        domestic_invoice_id = data.pop('domestic_invoice')
        warehousing_num = data.get('warehousing_num')
        existed = BranchWarehousing.objects.filter(warehousing_num=warehousing_num)
        if existed:
            self.instance = existed[0]
            existed.update(branch_stock_id=branch_stock_id,domestic_invoice_id=domestic_invoice_id, **data)
            if self.instance.status != 0:
                return False
            self.instance.domestic_invoice_product.all().delete()
        else:
            self.instance = DomesticInvoice.objects.create(branch_stock_id=branch_stock_id,domestic_invoice_id=domestic_invoice_id, **data)
        return self.instance



