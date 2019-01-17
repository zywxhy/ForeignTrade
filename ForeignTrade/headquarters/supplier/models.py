from django.db import models
from product.models import Product

#Create your models here.

class Supplier(models.Model):
    name = models.CharField(max_length=150,default='',unique=True,verbose_name='客户名')
    account_period = models.IntegerField(default=0,verbose_name='账期')
    area = models.CharField(max_length=50,default='',verbose_name='地区')
    address = models.CharField(max_length=200,default='',verbose_name='地址')
    eco_nature = models.CharField(max_length=20,default='',verbose_name='经济性质')
    bank_account = models.CharField(max_length=50,default='',verbose_name='银行账户')
    bank = models.CharField(max_length=50,default='',verbose_name='开户银行')
    duty_para = models.CharField(max_length=50,default='',verbose_name='税号')
    postalcode = models.CharField(max_length=50,default='',verbose_name='邮政编码')
    fax = models.CharField(max_length=50,default='',verbose_name='传真')
    telephone = models.CharField(max_length=50,default='',verbose_name='电话')
    inputting_date = models.DateField(verbose_name='建档时间')
    is_head_office = models.BooleanField(default=False,verbose_name='是否总公司')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '供应商'
        verbose_name_plural = verbose_name

class SupplierContacts(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,verbose_name='供应商')
    name = models.CharField(max_length=50,default='',verbose_name='联系人名字')
    phone = models.CharField(max_length=50,default='',verbose_name='联系电话')
    telephone = models.CharField(max_length=50,default='',verbose_name='手机号码')
    fax = models.CharField(max_length=50, default='', verbose_name='传真')
    email = models.CharField(max_length=50, default='', verbose_name='邮箱')
    position = models.CharField(max_length=50,default='',verbose_name='职位')
    master_contact = models.BooleanField(default=False,verbose_name='主联系人')

    def __str__(self):
        return self.supplier.name +':'+ self.name

    class Meta:
        verbose_name = '供应商相关联系人'
        verbose_name_plural = verbose_name

class SupplierProduct(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='供应商')
    product = models.ForeignKey(Product,on_delete=models.PROTECT,verbose_name='产品')

    def __str__(self):
        return self.supplier.name +':'+self.product.product_id+ ','+ self.product.name

    class Meta:
        verbose_name = '供应商产品'
        verbose_name_plural = verbose_name
