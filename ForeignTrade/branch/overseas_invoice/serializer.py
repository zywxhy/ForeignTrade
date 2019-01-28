from rest_framework.serializers import ModelSerializer,ListSerializer
from rest_framework import serializers
from rest_framework.serializers import ReturnDict,ReturnList
from .models import OverseasInvoice,OverseasInvoiceProduct
from domestic_invoice.serializer import ProductModelSerializer
from branch_sales.models import BranchSalesContract


# 国内发货单产品序列化类(嵌套产品信息)
class OverseasInvoiceProductModelSerializer(ModelSerializer):
    product = ProductModelSerializer(read_only=True)

    class Meta:
        model = OverseasInvoiceProduct
        fields = '__all__'

    def save(self, **kwargs):
        overseas_invoice = kwargs.pop('overseas_invoice')
        product_id = kwargs.pop('product_id')
        data = self.data
        self.instance = OverseasInvoiceProduct.objects.create(product_id=product_id,overseas_invoice=overseas_invoice,**data)
        return self.instance


# 国内发货单序列化类(嵌套发货单产品)
class OverseasInvoiceModelSerializer(ModelSerializer):
    overseas_invoice_product = OverseasInvoiceProductModelSerializer(many=True,read_only=True)
    overseas_invoice_num = serializers.CharField(max_length=30,default='',allow_null=False)

    class Meta:
        model = OverseasInvoice
        fields = '__all__'

    def save(self, **kwargs):
        data = self.data
        branch_stock_id = data.pop('branch_stock')
        sales_num = data.pop('sales_num')
        overseas_invoice_num = data.get('overseas_invoice_num')
        branch_sales = BranchSalesContract.objects.get(sales_num = sales_num)
        existed = OverseasInvoice.objects.filter(overseas_invoice_num=overseas_invoice_num)
        if existed:
            self.instance = existed[0]
            existed.update(branch_stock_id=branch_stock_id,branch_sales=branch_sales, **data)
            if self.instance.status != 0:
                return False
            self.instance.warehousing_product.all().delete()
        else:
            self.instance = OverseasInvoice.objects.create(branch_stock_id=branch_stock_id,branch_sales=branch_sales, **data)
        return self.instance



