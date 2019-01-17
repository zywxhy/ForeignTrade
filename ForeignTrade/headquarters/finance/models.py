from django.db import models
from datetime import date
from sales.models import SalesContract
from purchase.models import PurchaseContract
# Create your models here.


#  汇率，根据公司区分对人民币汇率还是对美元汇率
class ExchangeRate(models.Model):
    currency = models.CharField(max_length=50,verbose_name='币种')
    type = models.CharField(max_length=20,verbose_name='兑换货币')
    date = models.DateField(verbose_name='修改时间')
    exchange_rate = models.FloatField(default=1,verbose_name='汇率')

    class Meta:
        verbose_name = '汇率'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.currency+'/'+self.type+':'+str(self.exchange_rate)


# 实际收款表
class ActualReceipts(models.Model):
    sales = models.ForeignKey(SalesContract, on_delete=models.CASCADE, verbose_name='销售合同')
    receipt = models.FloatField(default=0, verbose_name='收款金额')
    receipt_type = models.CharField(max_length=30, verbose_name='收款方式')
    receipt_date = models.DateField(verbose_name='收款时间')
    remark = models.CharField(max_length=100, default='', verbose_name='备注')

    def __str__(self):
        return self.sales.sales_num + ':' + '收款计划'

    class Meta:
        verbose_name = '实际收款'
        verbose_name_plural = verbose_name


# 实际付款表
class ActualPayment(models.Model):
    purchase = models.ForeignKey(PurchaseContract, on_delete=models.CASCADE, verbose_name='采购合同')
    payment_amount = models.FloatField(default=0, verbose_name='付款金额')
    payment_type = models.CharField(max_length=30, verbose_name='付款方式')
    payment_date = models.DateField(verbose_name='付款时间')
    remark = models.CharField(max_length=100, default='', verbose_name='备注')

    def __str__(self):
        return self.purchase.purchase_num + ':' + '付款计划'

    class Meta:
        verbose_name = '实际付款'
        verbose_name_plural = verbose_name
