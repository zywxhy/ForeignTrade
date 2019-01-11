from rest_framework.serializers import ModelSerializer
from .models import BranchStock,BranchStockProducts,BranchStockRecord
from domestic_invoice.serializer import ProductModelSerializer


class BranchStockProductsModelSerializer(ModelSerializer):
    product = ProductModelSerializer()

    class Meta:
        model = BranchStockProducts
        exclude = ('unit_cost',)






class BranchStockModelSerializer(ModelSerializer):
    branch_stock_product = BranchStockProductsModelSerializer(many=True)

    class Meta:
        model = BranchStock
        fields = '__all__'