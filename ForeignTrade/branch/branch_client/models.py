from django.db import models
from users.models import MyUser
from django.utils.translation import ugettext_lazy as _
from datetime import date
# Create your models here.



# 海外分公司客户表
class BranchClient(models.Model):
    level = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')]

    salesman = models.ForeignKey(MyUser,on_delete=models.PROTECT,verbose_name=_('所属业务员'),help_text='所属业务员')  # 客户所属业务员(包含分公司信息)
    client_id = models.CharField(max_length=50, default='', unique=True, verbose_name='客户代码',help_text='客户代码')
    name = models.CharField(max_length=100, default='', verbose_name='客户名',help_text='客户名')
    company_name = models.CharField(max_length=100, default='', verbose_name='客户公司名',help_text='客户公司名')
    address = models.CharField(max_length=100, default='', verbose_name='客户地址',help_text='客户地址')
    tax_number = models.CharField(max_length=50, default='', verbose_name='税号',help_text='税号')
    credit = models.CharField(max_length=10,choices=level,default='5',verbose_name='客户信用',help_text='客户信用')
    level = models.CharField(max_length=10,choices=level,default='1',verbose_name='客户级别',help_text='客户级别')
    info = models.CharField(max_length=100, default='', verbose_name='客户信息',help_text='客户信息')
    recent_date = models.DateField(verbose_name='最近通讯时间',help_text='最近通讯时间')

    # 当前交易完成或询价后 更新最近联系时间
    def date_update(self,client):
        new_recent_date = date.today()
        client.recent_date = new_recent_date
        client.save()
        return True

    class Meta:
        verbose_name = '海外客户'
        verbose_name_plural = verbose_name


# 海外分公司联系人
class ClientContact(models.Model):
    branch_client = models.ForeignKey(BranchClient,on_delete=models.CASCADE,verbose_name='客户')
    email = models.CharField(max_length=50, default='', unique=True, verbose_name='邮箱')


