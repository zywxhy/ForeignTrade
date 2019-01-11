from rest_framework.serializers import ModelSerializer,ListSerializer
from rest_framework import serializers
from rest_framework.serializers import ReturnDict,ReturnList
from .models import OverseasInvoice,OverseasInvoiceProduct
from domestic_invoice.serializer import ProductModelSerializer










# 国内发货单产品序列化类(嵌套产品信息)
class OverseasInvoiceProductModelSerializer(ModelSerializer):

    class Meta:
        model = OverseasInvoiceProduct
        fields = '__all__'


    # 复写父类 data函数,将产品表字段加入到字典中，并返回
    @property
    def data(self):
        ret = super(serializers.Serializer, self).data
        my_dict = ReturnDict(ret, serializer=self)
        id = my_dict['product']
        product_data = ProductModelSerializer(instance=self.instance.product).data
        product_data.pop('id')
        my_dict.update(product_data)
        return my_dict





#国内发货单序列化类(嵌套发货单产品)
class OverseasInvoiceModelSerializer(ModelSerializer):
    overseas_invoice_product = OverseasInvoiceProductModelSerializer(many=True)
    overseas_invoice_num = serializers.CharField(max_length=30,default='',allow_null=False)


    class Meta:
        model = OverseasInvoice
        fields = '__all__'



        pass

    # 复写父类 data函数,将产品表字段加入到字典中，并返回
    @property
    def data(self):
        ret = super(serializers.Serializer, self).data
        my_dict = ReturnDict(ret, serializer=self)
        overseas_invoice_product = []
        try:
            overseas_invoice_product_set = self.instance.overseas_invoice_product.all()
        except:
            return my_dict
        for product in overseas_invoice_product_set:
            overseas_invoice_product.append(OverseasInvoiceProductModelSerializer(instance=product).data)

        my_dict.__setitem__('overseas_invoice_product',overseas_invoice_product)
        my_dict.__setitem__('status',0)
        return my_dict


    def create(self, validated_data):
        overseas_invoice_product = validated_data.pop('overseas_invoice_product')
        overseas_invoice_num = validated_data['overseas_invoice_num']
        existed = OverseasInvoice.objects.filter(overseas_invoice_num=overseas_invoice_num)
        if existed:
            existed.update(**validated_data)
            overseas_invoice = existed[0]
            overseas_invoice.overseas_invoice_product.all().delete()
        else:
            overseas_invoice = OverseasInvoice.objects.create(**validated_data)
        for product_item in overseas_invoice_product:
            product_id = product_item.pop('product')
            OverseasInvoiceProduct.objects.create(overseas_invoice=overseas_invoice,product_id=product_id, **product_item)
        return overseas_invoice



