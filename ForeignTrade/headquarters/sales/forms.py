from django import forms
from users.models import MyUser,Company
from sales.models import time_to_str,SalesContract
from finance.models import ExchangeRate
from client.models import Client
from django.db.models import Q
# 销售合同
class SalesForm(forms.Form):
    export_company_list = (('(Mexico)OPTICTIMES','(Mexico)OPTICTIMES'),('(PERU)OPTICTIMES S.A.C','(PERU)OPTICTIMES S.A.C'),
                           ('(china)optictimes.co.ltd','(china)optictimes.co.ltd'),
                           ('杭州易光科技有限公司', '杭州易光科技有限公司'),('杭州润州光电技术邮箱公司','杭州润州光电技术邮箱公司'))

    def __init__(self,user,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['salesman'].queryset = MyUser.objects.filter(type='salesman',company_id=user.company.id)
        


        currency = []
        if user.company.name == '润州光电':
            exrate = ExchangeRate.objects.filter(type='CNY')
            self.fields['client'].queryset = Client.objects.filter(Q(salesman_id=user.id)| Q(is_branch=True))
        else:
            exrate = ExchangeRate.objects.filter(type='USD')
            self.fields['client'].queryset = Client.objects.filter(salesman_id=user.id)
        for e in exrate:
            currency.append((e.currency, e.currency))

        self.fields['currency'].choices = currency

    # widget=forms.TextInput(attrs={'class': 'form-control'})
    price_clause_select = (('FOB','FOB'),('CIF','CIF'),('C&F','C&F'),('CFR','CFR'),('CCC','CCC'),)

    sales_num = forms.CharField(max_length=20,initial='S'+time_to_str(),
                                widget=forms.TextInput(attrs={'class': 'form-control','disabled':'disabled'}),label='合同编号',)
    salesman = forms.ModelChoiceField(queryset=MyUser.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}),empty_label="(Nothing)",label='业务员')
    buyer = forms.CharField(max_length=20,initial='',widget=forms.TextInput(attrs={'class': 'form-control'}),label='采购员')
    #maker = forms.CharField(max_length=20,initial='',widget=forms.TextInput(attrs={'class': 'form-control'}),label='制单人')
    date = forms.DateField(label='签约日期',widget=forms.TextInput(attrs={'class': 'form-control datepicker','autocomplete':"off"}))
    shipment_port  = forms.CharField(max_length=30, initial='', label='装运口岸',widget=forms.TextInput(attrs={'class': 'form-control'}))
    destination_port = forms.CharField(max_length=30,initial='',label='目的口岸',widget=forms.TextInput(attrs={'class': 'form-control'}))
    client = forms.ModelChoiceField(queryset=Client.objects.all(),widget=forms.Select(attrs={'class': 'form-control select2_sample',}),label='客户')
    currency = forms.ChoiceField(label='币种',widget=forms.Select(attrs={'class': 'form-control'}))
    price_clause = forms.ChoiceField(label='价格条款',choices=price_clause_select,
                                   widget=forms.Select(attrs={'class': 'form-control'}))   #外键获取价格条款from财务系统
    export_company = forms.ChoiceField(label='出口公司',choices=export_company_list,widget=forms.Select(attrs={'class': 'form-control'}))
    mode_of_transport = forms.ChoiceField(label='运输方式',choices=(('空运','空运'),('海运','海运'),('快递','快递')),
                                          widget=forms.Select(attrs={'class': 'form-control'}),)
    exrate = forms.FloatField(initial=1,label='汇率',widget=forms.TextInput(attrs={'class': 'form-control','disabled':'disabled'}))
    shipping_fee = forms.FloatField(min_value=0,initial=0,label='运费',widget=forms.NumberInput(attrs={'class': 'form-control changeable'}))
    insurance = forms.FloatField(min_value=0,initial=0,label='保险费',
                                 widget=forms.NumberInput(attrs={'class': 'form-control changeable'}))
    other_fee = forms.FloatField(min_value=0,initial=0,label='其他费用',widget=forms.NumberInput(attrs={'class': 'form-control changeable'}))
    total_amount = forms.FloatField(min_value=0,initial=0,label='总金额',widget=forms.NumberInput(attrs={'class': 'form-control','disabled':'disabled'}))
    remark = forms.CharField(max_length=300,initial='',label='备注',required=False,widget=forms.Textarea(attrs={'class': 'form-control',}))   #销售合同备注

#
# class SalesProduct(forms.Form):
#     sales_num = forms.CharField(max_length=20, initial=time_to_str(),
#                                 widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
#                                 label='合同编号', )
#     product_product_id = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='产品')
#     remark = models.CharField(max_length=200, default='', verbose_name='备注')
#     volume = models.FloatField(default=0, verbose_name='体积')
#     count = models.IntegerField(verbose_name='数量')
#     outbound_count = models.IntegerField(default=0, verbose_name='出库数量')
#     return_count = models.IntegerField(default=0, verbose_name='退货数量')
#     unit_price = models.FloatField(verbose_name='单价')
#     amount = models.FloatField(verbose_name='金额')
#     discount = models.FloatField(verbose_name='折扣')
#     receivable_amount = models.FloatField(verbose_name='应收金额')
#
#     status = models.IntegerField(default=0, verbose_name='预留字段')  # 预留字段


class SalesModelForm(forms.ModelForm):
    class Meta:
        model = SalesContract
        fields = ['sales_num','salesman','buyer','date','shipment_port','destination_port','client',
                  'currency','price_clause','export_company','mode_of_transport','exrate',
                  'shipping_fee','insurance','other_fee','total_amount','remark']
        widgets = {
            'sales_num': forms.TextInput(attrs={'class': 'form-control','disabled':'disabled'}),
            'salesman': forms.TextInput(attrs={'class': 'form-control','disabled':'disabled'}),
            'buyer': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'date': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'shipment_port': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'destination_port': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'client': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'mode_of_transport': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'currency': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'price_clause': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'export_company': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'exrate': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'shipping_fee': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'insurance': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'other_fee': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'total_amount': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'remark': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
        }







class SalesStatisticsForm(forms.Form):
    company = forms.ModelChoiceField(queryset=Company.objects.all(),label='公司',widget=forms.Select(attrs={'class': 'form-control'}))
    type = forms.ChoiceField(label='查询类型',choices=(('client','按客户'),('product','按产品'),),
                                          widget=forms.Select(attrs={'class': 'form-control'}),)

    client = forms.CharField(label='客户',widget=forms.Select(attrs={'class': 'form-control selectpicker','data-live-search':'true'}))
    product = forms.CharField(label='产品',widget=forms.Select(attrs={'class': 'form-control selectpicker','data-live-search':'true'}))






