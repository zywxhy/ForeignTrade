from django.db import models
from users.models import MyUser
from supplier.models import Supplier
from product.models import Product

# Create your models here.


class PurchaseContract(models.Model):
    purchase_status = ((0, '未审核'), (1, '已审核'), (2, '已入库(全部)'), (3, '已完成(付款完毕)'), (4, '已退货(全部)'))


    purchase_num = models.CharField(max_length=30,verbose_name='采购单号',unique=True,default='')
    sales_num = models.CharField(max_length=30, verbose_name='合同编号', default='')
    buyer = models.ForeignKey(MyUser,verbose_name='采购员',on_delete=models.PROTECT)
    date = models.CharField(max_length=30, verbose_name='采购时间', unique=True, default='')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name='供应商')
    account_period = models.IntegerField(default=0, verbose_name='账期')
    reviewer = models.CharField( max_length=50,verbose_name='审批人',default='')
    currency = models.CharField(max_length=30, verbose_name='币种',default='')
    exrate = models.FloatField(verbose_name='汇率', default=1)
    bill_name = models.CharField(max_length=30, verbose_name='开票名称', default='')
    bill_unit = models.CharField(max_length=30, verbose_name='开票单位', default='')
    bill_quantity = models.IntegerField(verbose_name='开票数量', default=0)
    bill_amount = models.FloatField(max_length=30, verbose_name='开票金额', default=0)
    not_bill_amount = models.FloatField(max_length=30, verbose_name='未开票金额', default=0)
    total_amount = models.FloatField(max_length=30, verbose_name='总金额',default=0)
    serial_number = models.IntegerField(default=1)  # 入库单序号，提交入库单会增加1
    status = models.IntegerField(default=0,choices=purchase_status,verbose_name='订单状态')

    def __str__(self):
        return self.buyer.first_name+':'+ self.purchase_num

    class Meta:
        verbose_name = '采购订单'
        verbose_name_plural = verbose_name



class PurchaseProduct(models.Model):
    purchase = models.ForeignKey(PurchaseContract,on_delete=models.CASCADE,verbose_name='采购合同')
    product = models.ForeignKey(Product,on_delete=models.PROTECT,verbose_name='产品')
    remark = models.CharField(max_length=200, default='',verbose_name='备注')
    count = models.IntegerField(verbose_name='数量')
    storage_count = models.IntegerField(default=0,verbose_name='入库数量')
    return_count = models.IntegerField(default=0,verbose_name='退货数量')
    unit_price = models.FloatField(verbose_name='单价')
    status = models.IntegerField(default=0,verbose_name='预留字段')  # 预留字段

    def __str__(self):
        return self.product.product_id

    class Meta:
        verbose_name = '订单内产品'
        verbose_name_plural = verbose_name