from rest_framework.serializers import ModelSerializer,ListSerializer
from rest_framework import serializers
from rest_framework.serializers import ReturnDict,ReturnList
from .models import OverseasInvoice,OverseasInvoiceProduct
from domestic_invoice.serializer import ProductModelSerializer










# 国内发货单产品序列化类(嵌套产品信息)
class OverseasInvoiceProductModelSerializer(ModelSerializer):
    product = ProductModelSerializer()
    class Meta:
        model = OverseasInvoiceProduct
        fields = '__all__'







#国内发货单序列化类(嵌套发货单产品)
class OverseasInvoiceModelSerializer(ModelSerializer):
    overseas_invoice_product = OverseasInvoiceProductModelSerializer(many=True)
    overseas_invoice_num = serializers.CharField(max_length=30,default='',allow_null=False)


    class Meta:
        model = OverseasInvoice
        fields = '__all__'





