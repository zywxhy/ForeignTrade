from rest_framework.serializers import ModelSerializer,ListSerializer
from rest_framework import serializers
from rest_framework.serializers import ReturnDict,ReturnList
from .models import DomesticInvoice,DomesticInvoiceProduct
from product.models import Product








#产品序列化类
class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ['type']



# 国内发货单产品序列化类(嵌套产品信息)
class DomesticInvoiceProductModelSerializer(ModelSerializer):
    product = ProductModelSerializer(allow_null=True)
    class Meta:
        model = DomesticInvoiceProduct
        fields = '__all__'



# 国内发货单序列化类(嵌套发货单产品)
class DomesticInvoiceModelSerializer(ModelSerializer):
    domestic_invoice_product = DomesticInvoiceProductModelSerializer(many=True)
    domestic_invoice_num = serializers.CharField(max_length=30,default='',)
    address = serializers.CharField(max_length=30,default='',allow_null=False)

    class Meta:
        model = DomesticInvoice
        fields = '__all__'






