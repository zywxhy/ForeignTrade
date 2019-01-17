from django.db import models
from branch_sales.models import BranchSalesContract
from product.models import Product
from branch_stock.models import BranchStock

# Create your models here.
class OverseasInvoice(models.Model):
    branch_sales = models.ForeignKey(BranchSalesContract,on_delete=models.PROTECT,verbose_name='销售订单',help_text='销售订单')
    overseas_invoice_num = models.CharField(max_length=50,verbose_name='出库单号',help_text='出库单号')
    invoice_date = models.DateField(default='2000-01-01',verbose_name='出库日期',help_text='出库日期')
    maker = models.CharField(max_length=30,verbose_name='经办人',help_text='经办人')
    remark = models.CharField(max_length=300,verbose_name='备注',help_text='备注')
    shipping_method = models.CharField(max_length=300,verbose_name='运输方式',help_text='运输方式')
    branch_stock = models.ForeignKey(BranchStock, on_delete=models.CASCADE, verbose_name='仓库')



class OverseasInvoiceProduct(models.Model):
    overseas_invoice = models.ForeignKey(OverseasInvoice,related_name='overseas_invoice_product',on_delete=models.CASCADE,verbose_name='出库单',help_text='出库单')
    product = models.ForeignKey(Product,on_delete=models.PROTECT,verbose_name='出库产品',help_text='出库产品')
    count = models.IntegerField(default=0,verbose_name='预计出库数量',help_text='预计出库数量')
    real_count = models.IntegerField(default=0,verbose_name='实际出库数量',help_text='实际出库数量')


