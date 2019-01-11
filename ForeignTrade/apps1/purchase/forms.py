from django import forms
from users.models import MyUser
from supplier.models import Supplier
from finance.models import ExchangeRate

class PurchaseForm(forms.Form):
    def __init__(self,request,*args, **kwargs):
        user = request.user
        super().__init__(*args, **kwargs)
        self.fields['buyer'].queryset = MyUser.objects.filter(type='buyer',company=user.company)
        currency = []
        if user.company.name == '润州光电':
            exrate = ExchangeRate.objects.filter(type='CNY')
        else:
            exrate = ExchangeRate.objects.filter(type='USD')
        for e in exrate:
            currency.append((e.currency,e.currency))

        self.fields['currency'].choices = currency


    purchase_num = forms.CharField(max_length=30,label='采购单号',widget=forms.TextInput(attrs={'class': 'form-control',}),)
    sales_num = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control',}),label='合同编号',)
    buyer = forms.ModelChoiceField(queryset=MyUser.objects.all(),widget=forms.Select(attrs={'class': 'form-control',}),label='采购员',)
    date = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control datepicker',}),label='采购时间',)
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(),widget=forms.Select(attrs={'class': 'form-control selectpicker', }) ,label='供应商')
    account_period = forms.IntegerField( widget=forms.TextInput(attrs={'class': 'form-control',}),label='账期')
    reviewer = forms.CharField(max_length=30, label='审批人',widget=forms.TextInput(attrs={'class': 'form-control',}), )
    currency = forms.ChoiceField(choices=[], label='币种',widget=forms.Select(attrs={'class': 'form-control',}),)
    exrate = forms.FloatField(label='汇率',widget=forms.NumberInput(attrs={'class': 'form-control','disabled':'disabled'}),)
    bill_name = forms.CharField(max_length=30, label='开票名称',widget=forms.TextInput(attrs={'class': 'form-control',}),  )
    bill_unit = forms.CharField(max_length=30, label='开票单位',widget=forms.TextInput(attrs={'class': 'form-control',}), )
    bill_quantity = forms.IntegerField(label='开票数量',widget=forms.NumberInput(attrs={'class': 'form-control',}),)
    bill_amount = forms.FloatField( label='开票金额',widget=forms.NumberInput(attrs={'class': 'form-control',}),)
    not_bill_amount = forms.FloatField(label='未开票金额',widget=forms.NumberInput(attrs={'class': 'form-control','disabled':'disabled'}), )
    total_amount = forms.FloatField(label='总金额', widget=forms.NumberInput(attrs={'class': 'form-control','disabled':'disabled'}),)
    remark = forms.CharField(label='备注', widget=forms.Textarea(attrs={'class': 'form-control',}),)