from django.db import models
from users.models import MyUser
from datetime import date,datetime
# Create your models here.
class ContinentsState(models.Model):
    continent_cname = models.CharField(max_length=50,default='',verbose_name='所在大洲')
    continent_name = models.CharField(max_length=50, default='',verbose_name='所在大洲(英文)')
    country_cname = models.CharField(max_length=50, default='',verbose_name='地区')
    country_name = models.CharField(max_length=50,default='',verbose_name='地区(英文)')
    is_parent = models.BooleanField(default=False)

    def __str__(self):
        return self.continent_name+':'+self.country_name

    class Meta:
        verbose_name = '大洲国家表'
        verbose_name_plural = verbose_name





class Client(models.Model):
    level = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')]

    area = models.ForeignKey(ContinentsState,related_name='area',on_delete=models.CASCADE,verbose_name='地区')
    client_id = models.CharField(max_length=50,default='',unique=True,verbose_name='客户代码')
    name =  models.CharField(max_length=100,default='',verbose_name='客户名')
    company_name = models.CharField(max_length=100,default='',verbose_name='客户公司名')
    credit = models.CharField(max_length=10,choices=level,default='5',verbose_name='客户信用')
    level = models.CharField(max_length=10,choices=level,default='1',verbose_name='客户级别')
    salesman = models.ForeignKey(MyUser,default=1,on_delete=models.CASCADE,verbose_name='客户所属分管人')  #确定一个分公司分管人
    info = models.CharField(max_length=100,default='', verbose_name='客户信息')
    is_branch = models.BooleanField(default=False,verbose_name='是否分公司')
    recent_date = models.DateField(verbose_name='最近时间')

    class Meta:
        verbose_name = '客户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ClientContact(models.Model):
    client = models.ForeignKey(Client,on_delete=models.CASCADE,verbose_name='客户')
    email = models.CharField(max_length=50, default='', unique=True, verbose_name='邮箱')
