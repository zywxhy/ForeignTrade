from django import forms
from users.models import MyUser, Company
from sales.models import time_to_str, SalesContract
from finance.models import ExchangeRate
from branch_client.models import BranchClient
from django.db.models import Q


# 销售订单(报价阶段)
class BranchSalesForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['salesman'].queryset = MyUser.objects.filter(type='salesman', company_id=user.company.id)


    # widget=forms.TextInput(attrs={'class': 'form-control'})
    sales_num = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class': 'form-control'}),label='合同编号', )
    salesman = forms.ModelChoiceField(queryset=MyUser.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}), empty_label="(Nothing)",
                                      label='业务员')

    # maker = forms.CharField(max_length=20,initial='',widget=forms.TextInput(attrs={'class': 'form-control'}),label='制单人')
    sales_date = forms.DateField(label='签约日期',
                           widget=forms.TextInput(attrs={'class': 'form-control datepicker', 'autocomplete': "off"}))

    client = forms.ModelChoiceField(queryset=BranchClient.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control select2_sample', }), label='客户')
    currency = forms.ChoiceField(label='币种', widget=forms.Select(attrs={'class': 'form-control'}))


    # exrate = forms.FloatField(initial=1, label='汇率',
    #                           widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}))
    shipping_fee = forms.FloatField(min_value=0, initial=0, label='运费',
                                    widget=forms.NumberInput(attrs={'class': 'form-control changeable'}))


    total_amount = forms.FloatField(min_value=0, initial=0, label='总金额',
                                    widget=forms.NumberInput(attrs={'class': 'form-control', 'disabled': 'disabled'}))
    remark = forms.CharField(max_length=300, initial='', label='备注', required=False,
                             widget=forms.Textarea(attrs={'class': 'form-control', }))  # 销售合同备注

