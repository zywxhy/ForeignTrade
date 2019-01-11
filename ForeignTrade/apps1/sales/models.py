from django.db import models
from users.models import Company,MyUser
from product.models import Product
from client.models import Client
import time,json
from django.core import serializers
# Create your models here.


# 自动生成销售合同号
def time_to_str():
    t = time.localtime()
    num = time.strftime("%Y%m%d%H%M", t)
    return num


# 销售合同
class SalesContract(models.Model):
    sales_status = ((0,'未审核'),(1,'已审核'),(2,'已采购'),(3,'已出库(全部)'),(4,'已完成(收款完毕)'),(5,'已退货(全部)'))

    sales_num = models.CharField(max_length=20,default='',unique=True,verbose_name='合同编号')
    salesman = models.ForeignKey(MyUser,on_delete=models.CASCADE,verbose_name='业务员')
    buyer = models.CharField(max_length=20,default='',verbose_name='采购员')
    maker = models.CharField(max_length=20,default='',verbose_name='制单人')
    date = models.DateField(verbose_name='签约日期')
    shipment_port  = models.CharField(max_length=30, default='', verbose_name='装运口岸')
    destination_port = models.CharField(max_length=30,default='',verbose_name='目的口岸')
    client = models.ForeignKey(Client,on_delete=models.PROTECT,verbose_name='客户')
    currency = models.CharField(max_length=20,verbose_name='币种')
    price_clause = models.CharField(max_length=10,verbose_name='价格条款')   #外键获取价格条款from财务系统
    export_company = models.CharField(max_length=20,verbose_name='出口公司')
    mode_of_transport = models.CharField(max_length=20,choices=(('空运','空运'),('海运','海运'),('快递','快递')),verbose_name='运输方式')
    exrate = models.FloatField(default=1,verbose_name='汇率')
    status = models.IntegerField(default=0,choices=sales_status,verbose_name='合同状态')     # 0:未审核 1;已审核  2:已采购   3:退回    4:已出库(全部)  5:已完成(收款完毕)
    shipping_fee = models.FloatField(default=0,verbose_name='运费')
    insurance = models.FloatField(default=0,verbose_name='保险费')
    other_fee = models.FloatField(default=0,verbose_name='其他费用')
    total_amount = models.FloatField(default=0,verbose_name='总金额')
    invoice_index = models.IntegerField(default=1,verbose_name='出库单序号')  # 出库单序号，提交出库单会增加1
    refund_index = models.IntegerField(default=1, verbose_name='退货单序号')  # 退货单序号，提交退货单会增加1
    remark = models.CharField(max_length=300,default='',verbose_name='备注')   #销售合同备注

    def __str__(self):
        return self.sales_num

    class Meta:
        verbose_name = '销售合同'
        verbose_name_plural = verbose_name


class SalesProduct(models.Model):
    sales = models.ForeignKey(SalesContract,on_delete=models.CASCADE,verbose_name='销售合同')
    product = models.ForeignKey(Product,on_delete=models.PROTECT,verbose_name='产品')
    remark = models.CharField(max_length=200, default='',verbose_name='备注')
    volume = models.FloatField(default=0 ,verbose_name='体积')
    count = models.IntegerField(verbose_name='数量')
    outbound_count = models.IntegerField(default=0,verbose_name='出库数量')
    return_count = models.IntegerField(default=0,verbose_name='退货数量')
    unit_price = models.FloatField(verbose_name='单价')
    amount = models.FloatField(verbose_name='金额')
    discount = models.FloatField(verbose_name='折扣',default=0)
    receivable_amount = models.FloatField(verbose_name='应收金额',default=0)

    status = models.IntegerField(default=0,verbose_name='预留字段')  # 预留字段

    def __str__(self):
        return self.product.product_id

    @staticmethod
    def sales_serializers(my_model):
        data = serializers.serialize('json',my_model)
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
            a.update({'total_count':a['count']})
            a['count'] = 0
            products.append(a)
        return products


    class Meta:
        verbose_name = '合同内产品'
        verbose_name_plural = verbose_name


class CollectionPlan(models.Model):
    sales = models.ForeignKey(SalesContract,on_delete=models.CASCADE,verbose_name='销售合同')
    receipt = models.FloatField(default=0,verbose_name='收款金额')
    receipt_type = models.CharField(max_length=30,verbose_name='收款方式')
    receipt_time = models.DateField(verbose_name='预计时间')
    remark = models.CharField(max_length=100,default='',verbose_name='备注')

    def __str__(self):
        return self.sales.sales_num+':'+'收款计划'

    class Meta:
        verbose_name = '收款计划'
        verbose_name_plural = verbose_name




class SalesStatistics(models.Model):
    company = models.ForeignKey(Company,on_delete=models.PROTECT,verbose_name='公司')
    client = models.ForeignKey(Client,on_delete=models.PROTECT,verbose_name='客户')
    product = models.ForeignKey(Product,on_delete=models.PROTECT,verbose_name='产品')
    count = models.IntegerField(default=0,verbose_name='数量')
    year = models.IntegerField(default=2018,verbose_name='年')
    month = models.IntegerField(default=1,verbose_name='月')
