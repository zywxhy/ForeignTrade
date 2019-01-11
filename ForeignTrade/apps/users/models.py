from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

#公司
class Company(models.Model):
    company_id = models.CharField(max_length=10,verbose_name='公司ID')    #总公司ID为1 后续以此类推
    name = models.CharField(max_length=50, unique=True, verbose_name='公司名')  # 公司
    remark = models.CharField(max_length=300,verbose_name='公司备注') #备注

    class Meta:
        verbose_name = '公司'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

#员工
class MyUser(AbstractUser):
    company = models.ForeignKey(Company,verbose_name='所在公司',on_delete=models.CASCADE)  # 公司
    language = models.CharField(max_length=20, default='Chinese', verbose_name='语言')
    type = models.CharField(max_length=30, choices=(('salesman','业务员'),
                                                   ('buyer','采购员'),
                                                   ('finance','财务'),
                                                   ('others','其他')),
                                                   verbose_name='员工类别')
    is_position_reviewer = models.BooleanField(default=False, verbose_name='部门审核',help_text='销售/采购合同的审核权限等')
    is_warehouse_reviewer = models.BooleanField(default=False, verbose_name='仓库审核')  # 仓库审核权限
    permission_level = models.IntegerField(default=1,verbose_name='权限等级')# 1: 业务员，采购员，仓管 2：业务主管 ，采购主管，海外技术人员 3 海外负责人 4 总经理


    class Meta:
        verbose_name = '员工'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.company.name+':'+self.first_name




class Person(models.Model):
    name = models.CharField(max_length=20, default='', verbose_name='名字')
    info = models.CharField(max_length=20, default='', verbose_name='信息')


class Ticket(models.Model):
    test = models.ForeignKey(Person,on_delete=models.CASCADE,verbose_name='测试')
    name = models.CharField(max_length=20, default='',verbose_name='票')



