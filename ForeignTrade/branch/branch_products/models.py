from django.db import models
from product.models import Product
from users.models import Company
# Create your models here.


BranchProduct = Product
#
#清关税率表
class ProductTaxRate(models.Model):
    company = models.ForeignKey(Company,on_delete=models.PROTECT,verbose_name='分公司')
    product = models.ForeignKey(Product,on_delete=models.PROTECT,verbose_name='产品')
    tax_rate = models.FloatField(default=0,verbose_name='税率')