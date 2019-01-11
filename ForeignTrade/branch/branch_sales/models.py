from django.db import models
from users.models import MyUser
from product.models import Product
from branch_client.models import BranchClient

# Create your models here.
# 海外销售合同
class BranchSalesContract(models.Model):
    sales_status = ((0,'报价阶段'),(1,'销售订单'),(2,'审核失败'),(3,'已出库(全部)'),(4,'已完成(收款完毕)'),(5,'欠款'),(6,'退货'),)

    sales_num = models.CharField(max_length=20,default='',unique=True,verbose_name='合同编号')
    salesman = models.ForeignKey(MyUser,on_delete=models.CASCADE,verbose_name='业务员')
    maker = models.CharField(max_length=20,default='',verbose_name='制单人')
    sales_date = models.DateField(verbose_name='签约日期')
    client = models.ForeignKey(BranchClient,on_delete=models.PROTECT,verbose_name='海外分公司客户')
    currency = models.CharField(max_length=20,verbose_name='币种')
    price_clause = models.CharField(max_length=10,verbose_name='价格条款')   #外键获取价格条款from财务系统
    status = models.IntegerField(default=0,choices=sales_status,verbose_name='合同状态')
    total_amount = models.FloatField(default=0,verbose_name='总金额')
    remark = models.CharField(max_length=300,default='',verbose_name='备注')   #销售合同备注

    def __str__(self):
        return self.sales_num

    class Meta:
        verbose_name = '分公司销售合同'
        verbose_name_plural = verbose_name


# 分公司销售合同产品表
class BranchSalesProduct(models.Model):
    branch_sales = models.ForeignKey(BranchSalesContract,related_name='branch_sales_product',on_delete=models.CASCADE,verbose_name='分公司销售合同')
    product = models.ForeignKey(Product,on_delete=models.PROTECT,verbose_name='产品')
    remark = models.CharField(max_length=200, default='',verbose_name='备注')
    sales_count = models.IntegerField(verbose_name='销售数量')
    outbound_count = models.IntegerField(default=0,verbose_name='出库数量')
    return_count = models.IntegerField(default=0,verbose_name='退货数量')
    unit_price = models.FloatField(verbose_name='单价')
    amount = models.FloatField(verbose_name='金额')
    discount = models.FloatField(verbose_name='折扣',default=0)
    receivable_amount = models.FloatField(verbose_name='应收金额',default=0)
    status = models.IntegerField(default=0,verbose_name='预留字段')  # 预留字段


class BranchSalesCollections(models.Model):
    pass