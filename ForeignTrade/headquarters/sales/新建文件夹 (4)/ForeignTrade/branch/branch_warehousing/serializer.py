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






class BranchWarehousingModelSerializer(ModelSerializer):
    warehousing_product = BranchWarehousingProductModelSerializer(many=True)
    class Meta:
        model = BranchWarehousing
        fields = '__all__'




