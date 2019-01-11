from django.db import models
from users.models import MyUser
from supplier.models import Supplier
from product.models import Product
from django.core import serializers
import json
from datetime import date
# Create your models here.


class PurchaseContract(models.Model):
    purchase_status = ((0, '未审核'), (1, '已审核'), (2, '已入库(全部)'), (3, '已完成(付款完毕)'), (4, '已退货(全部)'))
    purchase_num = models.CharField(max_length=30,verbose_name='采购单号',unique=True,default='')
    sales_num = models.CharField(max_length=30, verbose_name='合同编号', default='')
    buyer = models.ForeignKey(MyUser,verbose_name='采购员',on_delete=models.PROTECT)
    date = models.DateField( verbose_name='采购时间', default=date(1970,1,1))
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name='供应商')
    account_period = models.IntegerField(default=0, verbose_name='账期')
    reviewer = models.CharField( max_length=50,verbose_name='审批人',default='')
    currency = models.CharField(max_length=30, verbose_name='币种',default='')
    exrate = models.FloatField(verbose_name='汇率', default=1)
    bill_name = models.CharField(max_length=30, verbose_name='开票名称', default='',null=True)
    bill_unit = models.CharField(max_length=30, verbose_name='开票单位', default='',null=True)
    bill_quantity = models.IntegerField(verbose_name='开票数量', default=0,null=True)
    bill_amount = models.FloatField(max_length=30, verbose_name='开票金额', default=0,null=True)
    not_bill_amount = models.FloatField(max_length=30, verbose_name='未开票金额', default=0,null=True)
    total_amount = models.FloatField(max_length=30, verbose_name='总金额',default=0)
    serial_number = models.IntegerField(default=1)  # 入库单序号，提交入库单会增加1
    remark = models.CharField(max_length=500,verbose_name='备注',default='')
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
    purchase_count = models.IntegerField(verbose_name='采购数量')
    storage_count = models.IntegerField(default=0,verbose_name='入库数量')
    return_count = models.IntegerField(default=0,verbose_name='退货数量')
    unit_price = models.FloatField(verbose_name='单价')
    amount = models.FloatField(default=0,verbose_name='金额')
    status = models.IntegerField(default=0,verbose_name='预留字段')  # 预留字段

    def __str__(self):
        return self.product.product_id

    class Meta:
        verbose_name = '订单内产品'
        verbose_name_plural = verbose_name

    @staticmethod
    def sales_serializers(my_model):
        data = serializers.serialize('json', my_model)
        data = json.loads(data)
        products = []
        for item in data:
            a = {}
            p = Product.objects.get(id=item['fields'].get('product'))
            for key2, value2 in p.__dict__.items():
                if key2 == 'count':
                    a['total_count'] = value2
                else:
                    a[key2] = value2
            for key, value in item['fields'].items():
                a[key] = value

            a.pop('_state')
            a.pop('image')
            a.pop('cost')
            a.update({'total_count': a['count']})
            a['count'] = 0
            products.append(a)
        return products





class Payment(models.Model):
    purchase = models.ForeignKey(PurchaseContract, on_delete=models.CASCADE, verbose_name='采购合同')
    payment_amount = models.FloatField(default=0, verbose_name='付款金额')
    payment_type = models.CharField(max_length=30, verbose_name='付款方式')
    payment_date = models.DateField(verbose_name='预计时间')
    remark = models.CharField(max_length=100, default='', verbose_name='备注')

    def __str__(self):
        return self.purchase.purchase_num + ':' + '付款计划'

    class Meta:
        verbose_name = '付款计划'
        verbose_name_plural = verbose_name
