from django.db import models
from branch_client.models import BranchClient
# Create your models here.
class BranchInquiry(models.Model):
    branch_inquiry_num = models.CharField(max_length=20,unique=True,default='',verbose_name='询价单号')
    branch_client = models.ForeignKey(BranchClient,on_delete=models.PROTECT,verbose_name='客户')
    inquiry_date = models.DateField(verbose_name='询价日期')



class BranchInquiryProduct(models.Model):
    branch_inquiry = models.ForeignKey(BranchInquiry,on_delete=models.CASCADE,verbose_name='询价单')
    model = models.CharField(max_length=20, default='', verbose_name='型号')
    name = models.CharField(max_length=50, default='', verbose_name='名称')
    spec = models.CharField(max_length=100, default='', verbose_name='规格要求')
    count = models.IntegerField(default=0, verbose_name='数量')
    mesu_unit = models.CharField(max_length=10, verbose_name='单位')
    package = models.CharField(max_length=60, verbose_name='包装要求')
    unit_price = models.FloatField(default=0, verbose_name='单价')
    remark = models.CharField(max_length=100, verbose_name='备注')
