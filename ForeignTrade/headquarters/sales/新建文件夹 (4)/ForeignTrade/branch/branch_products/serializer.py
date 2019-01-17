from rest_framework.serializers import ModelSerializer
from product.models import Product
from domestic_invoice.serializer import ProductModelSerializer


BranchProductModelSerializer = ProductModelSerializer
BranchProduct = Product
