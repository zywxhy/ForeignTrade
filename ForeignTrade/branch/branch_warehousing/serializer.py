from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import BranchWarehousing,BranchWarehousingProduct
from domestic_invoice.serializer import ProductModelSerializer,DomesticInvoice,Product
from rest_framework.routers import SimpleRouter
from rest_framework.serializers import ReturnDict,ReturnList

class BranchWarehousingProductModelSerializer(ModelSerializer):
    product = ProductModelSerializer()

    class Meta:
        model = BranchWarehousingProduct
        fields = '__all__'

    @property
    def data(self):
        ret = super(serializers.Serializer, self).data
        my_dict = ReturnDict(ret, serializer=self)
        id = my_dict['product']
        product_data = ProductModelSerializer(instance=self.instance.product).data
        product_data.pop('id')
        my_dict.update(product_data)
        return my_dict




class BranchWarehousingModelSerializer(ModelSerializer):
    warehousing_product = BranchWarehousingProduct()

    class Meta:
        model = BranchWarehousing
        fields = '__all__'

    @property
    def data(self):
        ret = super(serializers.Serializer, self).data
        my_dict = ReturnDict(ret, serializer=self)
        warehousing_product = []
        try:
            warehousing_product_Q = self.instance.domestic_invoice_product.all()
        except:
            return my_dict
        for product in warehousing_product_Q:
            warehousing_product.append(BranchWarehousingProductModelSerializer(instance=product).data)

        my_dict.__setitem__('warehousing_product', warehousing_product)
        my_dict.__setitem__('status', 0)
        return my_dict



    def create(self, validated_data):
        domestic_invoice_num = validated_data.pop('domestic_invoice_num')
        domestic_invoice = DomesticInvoice.objects.get(domestic_invoice_num=domestic_invoice_num)
        branch_warehousing_product = validated_data.pop('branch_warehousing_product')
        result = BranchWarehousing.objects.get_or_create(domestic_invoice=domestic_invoice,**validated_data)
        if not result[1]:
            branch_warehousing = BranchWarehousing.objects.filter(id=result[0].id)
            branch_warehousing.update(**validated_data)
            branch_warehousing = branch_warehousing[0]
            branch_warehousing.warehousing_product.all().delete()
        else:
            branch_warehousing = result[0]

        for product_item in branch_warehousing_product:
            pk = product_item.pop('id')
            product = Product.objects.get(pk=pk)
            BranchWarehousingProduct.objects.create(branch_warehousing=branch_warehousing,product=product,**product_item)

        return branch_warehousing


