from django.db import models
from users.models import Company
from product.models import Product

# Create your models here.
class BranchStock(models.Model):
    company = models.ForeignKey(Company,on_delete=models.PROTECT,verbose_name='所属公司')
    name = models.CharField(max_length=50,default='',unique=True,verbose_name='仓库名')

    class Meta:
        verbose_name = '仓库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.company.name + ':'+ self.name


class BranchStockProducts(models.Model):
    stock = models.ForeignKey(BranchStock, related_name='branch_stock_product',on_delete=models.PROTECT, verbose_name='仓库')
    product = models.ForeignKey(Product,on_delete=models.PROTECT,verbose_name='库存产品')
    count = models.IntegerField(default=0, verbose_name='总数量')
    sr_count = models.IntegerField(default=0, verbose_name='在途数量')
    por_count = models.IntegerField(default=0, verbose_name='需求数量')
    unit_cost = models.FloatField(default=0, verbose_name='平均成本')
    bad_count = models.IntegerField(default=0, verbose_name='不良品数量')
    recent_date = models.DateField(default='2000-01-01',verbose_name='最近入库时间')




class BranchStockRecord(models.Model):
    stock = models.ForeignKey(BranchStock, on_delete=models.PROTECT, verbose_name='仓库')
    maker = models.CharField(max_length=20, verbose_name='申请人')
    reviewer = models.CharField(max_length=20, verbose_name='审批人')
    odd_num = models.CharField(max_length=20, verbose_name='单号')
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='产品')
    unit_price = models.FloatField(default=0, verbose_name='售价')
    cost_unit_price = models.FloatField(default=0, verbose_name='成本')
    count = models.IntegerField(default=0, verbose_name='数量')
    type = models.IntegerField(default=0, choices=((0, '出库'), (1, '入库')), verbose_name='类型')
    reason = models.CharField(max_length=300, default='normal', verbose_name='原因')  # 出/入库原因
    date = models.DateField(default='2000-01-01',verbose_name='日期')
