from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from branch_products.serializer import ProductModelSerializer
from rest_framework.serializers import ReturnDict
from .models import BranchSalesProduct,BranchSalesContract,BranchSalesCollections


class BranchSalesProductModelSerializer(ModelSerializer):
    product = ProductModelSerializer(allow_null=True,read_only=True)
    class Meta:
        model = BranchSalesProduct
        fields = '__all__'
        pass

    def save(self, **kwargs):
        branch_sales = kwargs.pop('branch_sales')
        data = self.data
        #print(data)
        product_id = kwargs.pop('product_id')
        self.instance = BranchSalesProduct.objects.create(product_id=product_id,branch_sales=branch_sales, **data)
        return self.instance


class BranchSalesCollectionsModelSerializer(ModelSerializer):
    class Meta:
        model = BranchSalesCollections
        fields = '__all__'
        pass



class BranchSalesContractModelSerializer(ModelSerializer):
    branch_sales_product = BranchSalesProductModelSerializer(many=True,read_only=True)

    class Meta:
        model =  BranchSalesContract
        fields = '__all__'

    def save(self, **kwargs):
        data = self.data  # 这里嵌套的product信息会自动在key值上加[]，如：'id' 变成 '[id]' 后续处理要注意
        salesman_id = data.pop('salesman')
        client_id = data.pop('client')
        sales_num = data['sales_num']
        existed = BranchSalesContract.objects.filter(sales_num=sales_num)
        if existed:
            self.instance = existed[0]
            if self.instance.status != 0:
                return False
            existed.update(salesman_id=salesman_id,client_id=client_id, **data)
            self.instance.branch_sales_product.all().delete()
        else:
            self.instance = BranchSalesContract.objects.create(salesman_id=salesman_id,client_id=client_id, **data)
        return self.instance



