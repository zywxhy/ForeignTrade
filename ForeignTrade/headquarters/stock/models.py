from django.db import models
from django.db.models import Q
from users.models import Company,MyUser
from product.models import Product
from sales.models import SalesProduct
from purchase.models import PurchaseProduct
from collections import defaultdict

# Create your models here.
class Stock(models.Model):
    company = models.ForeignKey(Company,verbose_name='所在公司',on_delete=models.PROTECT)
    name = models.CharField(max_length=50,null=False,verbose_name='仓库名')

    class Meta:
        verbose_name = '仓库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class StockProduct(models.Model):
    product_status = ((0, '良品'), (1, '不良品'), (2, '报废品'))

    stock = models.ForeignKey(Stock, on_delete=models.PROTECT, verbose_name='仓库')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='产品')
    count = models.IntegerField(default=0,verbose_name='总数量')
    sr_count = models.IntegerField(default=0,verbose_name='在途数量')
    por_count = models.IntegerField(default=0,verbose_name='需求数量')
    unit_cost = models.FloatField(default=0,verbose_name='平均成本')
    bad_count = models.IntegerField(default=0,verbose_name='不良品数量')
    recent_date = models.DateField(verbose_name='最近入库时间')

    class Meta:
        verbose_name = '仓库产品'
        verbose_name_plural = verbose_name

    def mrp(self,stock_id):
        company_id = Stock.objects.get(stock_id = stock_id).company_id
        mrp_dict = defaultdict(lambda:[0,0])
        for product in SalesProduct.objects.filter(Q(sales__status=0)| Q(sales__status=1) | Q(sales__status=2),sales__salesman__company_id=company_id):
            mrp_dict[product.id][0] +=product.count -product.outbound_count
        for product in PurchaseProduct.objects.filter(Q(sales__status=0)| Q(sales__status=1) | Q(sales__status=2),purchase__buyer__company_id=company_id):
            mrp_dict[product.id][1] += product.count - product.outbound_count
        for key,value in mrp_dict.items():
            try:
                product = StockProduct.objects.get(product_id=key,stock_id=stock_id)
                product.sr_count = value[1]
                product.por_count = value[0]
                product.save()
            except Exception as e:
                pass
        return True





class StockRecord(models.Model):
    stock = models.ForeignKey(Stock,on_delete=models.PROTECT,verbose_name='仓库')
    maker = models.CharField(max_length=20, verbose_name='申请人')
    reviewer = models.CharField(max_length=20,verbose_name='审核人')
    order_num = models.CharField(max_length=20,verbose_name='单号')
    product_id = models.ForeignKey(Product,on_delete=models.PROTECT,verbose_name='产品')
    unit_price = models.FloatField(default=0,verbose_name='售价')
    cost_unit_price = models.FloatField(default=0,verbose_name='成本')
    count =models.IntegerField(default=0,verbose_name='数量')
    in_or_out = models.IntegerField(default=0,choices=((0, '出库'),(1, '入库')),verbose_name='出/入库')
    reason = models.CharField(max_length=300,default='normal',verbose_name='原因')   #出/入库原因
    date = models.DateField(verbose_name='日期')


