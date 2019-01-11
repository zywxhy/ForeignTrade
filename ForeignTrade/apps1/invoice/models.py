from django.db import models
from sales.models import SalesContract
from product.models import Product

# Create your models here.
class Invoice(models.Model):
    invoice_status = ((0, '未审核'), (1, '已出库'), (2, '审核未通过'), (3, '已退货(全部)'))

    invoice_num = models.CharField(max_length=50,unique=True,default='',verbose_name='出库单号')
    sales = models.ForeignKey(SalesContract,on_delete=models.PROTECT,verbose_name='销售合同')
    maker = models.CharField(max_length=50,default='',verbose_name='经办人')
    invoice_date = models.DateField(verbose_name='出库日期')
    ship_method = models.CharField(max_length=50,choices=(('空运','空运'),('海运','海运'),('快递','快递')),verbose_name='运输方式')
    manifest_num =  models.CharField(max_length=50,default='',verbose_name='发货单号')
    contact = models.CharField(max_length=100,default='',verbose_name='联系方式')
    address = models.CharField(max_length=150,default='',verbose_name='地址')
    status = models.IntegerField(default=0, choices=invoice_status, verbose_name='出库状态')

    def __str__(self):
        return self.invoice_num

    class Meta:
        verbose_name = '出库单'
        verbose_name_plural = verbose_name

class InvoiceProduct(models.Model):
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE,verbose_name='出库单')
    product = models.ForeignKey(Product,on_delete=models.PROTECT,verbose_name='产品')
    remark = models.CharField(max_length=200, default='', verbose_name='备注')
    count = models.IntegerField(verbose_name='数量')
    unit_price = models.FloatField(verbose_name='单价')
    cost = models.FloatField(default=0,verbose_name='成本')
    status = models.IntegerField(default=0, verbose_name='预留字段')  # 预留字段

    def __str__(self):
        return self.invoice.invoice_num+':'+self.product.product_id

    class Meta:
        verbose_name = '出库单产品'
        verbose_name_plural = verbose_name








