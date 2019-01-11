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


    # 复写父类 data函数,将产品表字段加入到字典中，并返回
    # @property
    # def data(self):
    #     ret = super(serializers.Serializer, self).data
    #     my_dict = ReturnDict(ret, serializer=self)
    #     id = my_dict['product']
    #     product_data = ProductModelSerializer(instance=self.instance.product).data
    #     product_data.pop('id')
    #     my_dict.update(product_data)
    #     return my_dict





# 国内发货单序列化类(嵌套发货单产品)
class DomesticInvoiceModelSerializer(ModelSerializer):
    domestic_invoice_product = DomesticInvoiceProductModelSerializer(many=True)
    domestic_invoice_num = serializers.CharField(max_length=30,default='',allow_null=True)
    address = serializers.CharField(max_length=30,default='',allow_null=False)

    class Meta:
        model = DomesticInvoice
        fields = '__all__'




    # 复写父类 data函数,将产品表字段加入到字典中，并返回
    # @property
    # def data(self):
    #     ret = super(serializers.Serializer, self).data
    #     my_dict = ReturnDict(ret, serializer=self)
    #     domestic_invoice_product = []
    #     try:
    #         domestic_invoice_product_Q = self.instance.domestic_invoice_product.all()
    #     except:
    #         return my_dict
    #     for product in domestic_invoice_product_Q:
    #         domestic_invoice_product.append(DomesticInvoiceProductModelSerializer(instance=product).data)
    #
    #     my_dict.__setitem__('domestic_invoice_product',domestic_invoice_product)
    #     my_dict.__setitem__('status',0)
    #     return my_dict


    # def create(self, validated_data):
    #     domestic_invoice_product = validated_data.pop('domestic_invoice_product')
    #     domestic_invoice_num = validated_data['domestic_invoice_num']
    #     existed = DomesticInvoice.objects.filter(domestic_invoice_num=domestic_invoice_num)
    #     if existed:
    #         existed.update(**validated_data)
    #         domestic_invoice = existed[0]
    #         domestic_invoice.domestic_invoice_product.all().delete()
    #     else:
    #         domestic_invoice = DomesticInvoice.objects.create(**validated_data)
    #     for product_item in domestic_invoice_product:
    #         product_id = product_item.pop('product')
    #         DomesticInvoiceProduct.objects.create(domestic_invoice=domestic_invoice,product_id=product_id, **product_item)
    #     return domestic_invoice


