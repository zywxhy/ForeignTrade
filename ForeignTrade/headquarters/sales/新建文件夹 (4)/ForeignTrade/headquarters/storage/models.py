from django.db import models
from purchase.models import PurchaseContract
from users.models import MyUser
from product.models import Product
# Create your models here.

class Storage(models.Model):   # 入库单 需添加仓库ID
    storage_status = ((0, '未审核'), (1, '已入库'), (2, '审核未通过'), (3, '已退货(全部)'))

    storage_num = models.CharField(max_length=50,unique=True,verbose_name='入库单号')
    purchase = models.ForeignKey(PurchaseContract,on_delete=models.CASCADE,verbose_name='采购单号')
    maker = models.CharField(max_length=50,default='',verbose_name='制单人')
    storage_date = models.DateField(verbose_name='入库日期')
    purchase_amount = models.FloatField(default=0,verbose_name='采购金额')
    arrival_date = models.DateField(verbose_name='到港日期',null=True)
    clearance_date = models.DateField(verbose_name='清关日期',null=True)

    status = models.IntegerField(default=0,choices=storage_status,verbose_name='入库状态')
    remark = models.CharField(default='',max_length=500,verbose_name='备注')

    def __str__(self):
        return self.storage_num

    class Meta:
        verbose_name = '入库单'
        verbose_name_plural = verbose_name



class StorageProduct(models.Model):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, verbose_name='入库单')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='产品')
    remark = models.CharField(max_length=200, default='', verbose_name='备注')
    count = models.IntegerField(default=0,verbose_name='入库数量')
    plan_count = models.IntegerField(verbose_name='计划入库数量')
    share_cost = models.FloatField(verbose_name='均摊成本',default=0)
    add_cost =  models.FloatField(verbose_name='额外成本',default=0)
    status = models.IntegerField(default=0, verbose_name='预留字段')  # 预留字段



    def __str__(self):
        return self.product.product_id

    class Meta:
        verbose_name = '入库产品'
        verbose_name_plural = verbose_name



