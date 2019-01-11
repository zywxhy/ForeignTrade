from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from branch_products.serializer import ProductModelSerializer
from rest_framework.serializers import ReturnDict
from .models import BranchSalesProduct,BranchSalesContract,BranchSalesCollections


class BranchSalesProductModelSerializer(ModelSerializer):
    class Meta:
        model = BranchSalesProduct
        fields = '__all__'
        pass


class BranchSalesCollectionsModelSerializer(ModelSerializer):
    class Meta:
        model = BranchSalesCollections
        fields = '__all__'
        pass



class BranchSalesContractModelSerializer(ModelSerializer):
    pass

    class Meta:
        model =  BranchSalesContract
        fields = '__all__'

    @property
    def data(self):
        ret = super(serializers.Serializer, self).data
        my_dict = ReturnDict(ret, serializer=self)
        branch_sales_product = []
        try:
            branch_sales_product_Q = self.instance.branch_sales_product.all()
        except:
            return my_dict
        for product in branch_sales_product_Q:
            branch_sales_product.append(BranchSalesProductModelSerializer(instance=product).data)

        my_dict.__setitem__('domestic_invoice_product', branch_sales_product)
        my_dict.__setitem__('status', 0)
        return my_dict

