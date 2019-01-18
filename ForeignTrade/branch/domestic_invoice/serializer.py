from rest_framework.serializers import ModelSerializer,ListSerializer
from rest_framework import serializers
from rest_framework.serializers import ReturnDict,ReturnList
from .models import DomesticInvoice,DomesticInvoiceProduct
from product.models import Product
import numbers







#产品序列化类
class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ['type']






def my_validator(value):
    try:
        value = float(value)
    except:
        raise serializers.ValidationError('The count or unit_price of the product must be a number.')

    if value <= 0:
        raise serializers.ValidationError('The amount or quantity of the product must be greater than 0.')




# 国内发货单产品序列化类(嵌套产品信息)
class DomesticInvoiceProductModelSerializer(ModelSerializer):
    product = ProductModelSerializer(allow_null=True, read_only=True,)

    class Meta:
        model = DomesticInvoiceProduct
        fields = '__all__'
        extra_kwargs = {
                        'count': {'validators': [my_validator]},
                        'unit_price':{'validators':[my_validator]}
                        }





    def save(self, **kwargs):
        domestic_invoice = kwargs.pop('domestic_invoice')
        data = self.data  # 这里嵌套的product信息会自动在key值上加[]，如：'id' 变成 '[id]' 后续处理要注意
        #print(data)
        product_id = kwargs.pop('product_id')
        self.instance = DomesticInvoiceProduct.objects.create(product_id=product_id,domestic_invoice=domestic_invoice, **data)
        return self.instance












# 国内发货单序列化类(嵌套发货单产品)
class DomesticInvoiceModelSerializer(ModelSerializer):
    domestic_invoice_product = DomesticInvoiceProductModelSerializer(many=True,read_only=True)
    domestic_invoice_num = serializers.CharField(max_length=30,default='',)
    address = serializers.CharField(max_length=30,default='',allow_null=False)

    class Meta:
        model = DomesticInvoice
        fields = '__all__'



    def save(self, **kwargs):
        data = self.data  # 这里嵌套的product信息会自动在key值上加[]，如：'id' 变成 '[id]' 后续处理要注意
        company_id = data.pop('company')
        domestic_invoice_num = data['domestic_invoice_num']
        existed = DomesticInvoice.objects.filter(domestic_invoice_num=domestic_invoice_num)
        if existed:
            existed.update(company_id=company_id, **data)
            self.instance = existed[0]
            self.instance.domestic_invoice_product.all().delete()
        else:
            self.instance = DomesticInvoice.objects.create(company_id=company_id, **data)
        return self.instance

