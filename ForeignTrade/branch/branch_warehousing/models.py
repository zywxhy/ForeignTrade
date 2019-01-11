from django.db import models
from domestic_invoice.models import DomesticInvoice,DomesticInvoiceProduct
from branch_stock.models import BranchStock,BranchStockProducts
from product.models import Product
# Create your models here.
#入库
class BranchWarehousing(models.Model):
    warehousing_num = models.CharField(max_length=20,default='',unique=True,verbose_name='入库单号')
    domestic_invoice = models.ForeignKey(DomesticInvoice,on_delete=models.CASCADE,verbose_name='国内发货单')
    branch_stock = models.ForeignKey(BranchStock,on_delete=models.CASCADE,verbose_name='仓库')
    warehousing_date = models.DateField(default='2000-01-01',verbose_name='入库时间',)
    share_cost = models.FloatField(default=0, verbose_name='均摊总成本')
    status = models.IntegerField(default=0,verbose_name='入库状态')   # 审批
    remark = models.CharField(default='', max_length=500, verbose_name='备注')


class BranchWarehousingProduct(models.Model):
    warehousing = models.ForeignKey(BranchWarehousing,on_delete=models.CASCADE,related_name='warehousing_product',verbose_name='海外入库单')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='入库产品')
    total_cost_price = models.FloatField(default=0,verbose_name='总成本',help_text='总成本')
    count = models.IntegerField(default=0, verbose_name='入库数量')
    remark = models.CharField(default='', max_length=200, verbose_name='备注',null=True)


