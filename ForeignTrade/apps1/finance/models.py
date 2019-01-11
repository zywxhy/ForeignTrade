from django.db import models
from _datetime import datetime
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
