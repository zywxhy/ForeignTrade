from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from branch_products.serializer import ProductModelSerializer
from rest_framework.serializers import ReturnDict
from .models import BranchSalesProduct,BranchSalesContract,BranchSalesCollections


class BranchSalesProductModelSerializer(ModelSerializer):
    product = ProductModelSerializer(allow_null=True)
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
    domestic_invoice_product = BranchSalesProductModelSerializer(many=True)

    class Meta:
        model =  BranchSalesContract
        fields = '__all__'



