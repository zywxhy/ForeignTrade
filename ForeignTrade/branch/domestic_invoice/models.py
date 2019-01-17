from django.db import models
from product.models import Product
from users.models import Company,MyUser
from datetime import date
# Create your models here.

# 海外备货，国内发货单
class DomesticInvoice(models.Model):
    company = models.ForeignKey(Company,on_delete=models.PROTECT,verbose_name='备货分公司') #当前国内发货目的分公司(备货分公司）
    domestic_invoice_num = models.CharField(max_length=30,default='',unique=True,verbose_name='国内发货单单号')
    invoice_date = models.DateField(default='2000-01-01',verbose_name='发货时间')
    estimated_date = models.DateField(default='2000-01-01',verbose_name='预计到达时间')
    method = models.CharField(max_length=15)
    freight = models.FloatField(default=0,verbose_name='运费')
    address = models.CharField(max_length=30,null=True,verbose_name='地址')
    bill = models.CharField(max_length=30,default='',verbose_name='提单号')
    arrival_date = models.DateField(default='2000-01-01', verbose_name='到港日期', null=True)
    clearance_date = models.DateField(default='2000-01-01', verbose_name='清关日期', null=True)
    share_cost = models.FloatField(default=0, verbose_name='均摊总成本')
    status = models.IntegerField(default=0)          # {0:'未审批,1:'已审批',2:'开始入库',3:'入库完毕'}
    remark = models.CharField(max_length=30,default='',verbose_name='其他信息')

#国内发货单产品表
class DomesticInvoiceProduct(models.Model):
    domestic_invoice = models.ForeignKey(DomesticInvoice,related_name='domestic_invoice_product',on_delete=models.CASCADE,verbose_name='国内发货单')
    product = models.ForeignKey(Product,related_name='product',on_delete=models.PROTECT,verbose_name='发货产品')
    count = models.IntegerField(default=0,verbose_name='发货数量')
    warehousing_count = models.IntegerField(default=0,verbose_name='入库数量')
    unit_price = models.FloatField(default=0,verbose_name='海外成本(国内报价)')
    share_cost = models.FloatField(verbose_name='均摊成本', default=0)
    add_cost = models.FloatField(verbose_name='额外成本', default=0)
    remark = models.CharField(max_length=100,default='',verbose_name='备注')


# 运输信息
class ShippingInfo(models.Model):
    domestic_invoice = models.ForeignKey(DomesticInvoice,on_delete=models.CASCADE,verbose_name='发货单号')
    sender = models.CharField(max_length=30,default='',verbose_name='发送人')
    receiver = models.ForeignKey(MyUser,on_delete=models.PROTECT,verbose_name='接收人')
    info = models.CharField(max_length=300,default='',verbose_name='运输信息')


