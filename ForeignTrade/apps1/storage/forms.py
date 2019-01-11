from django import forms
from users.models import MyUser
from purchase.models import PurchaseContract

class StorageAddForm(forms.Form):
    def __init__(self,request,*args,**kwargs):
        super().__init__()
        purchase = PurchaseContract.objects.get(purchase_num=request.GET['purchase_num'])
        self.fields['purchase_num'].initial = purchase.purchase_num
        self.fields['storage_num'].initial = 'W'+purchase.purchase_num[1:]
        #self.fields['']


    storage_num = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','disabled':'disabled'}), label='入库单号')
    purchase_num = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','disabled':'disabled'}),label='采购单号')
    maker = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','disabled':'disabled'}),label='制单人')
    reviewer = forms.ModelChoiceField(queryset=MyUser.objects.all(),widget=forms.Select(attrs={'class': 'form-control',}),label='审核人')
    warehouse_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control datepicker',}),label='入库日期')
    purchase_amount = forms.FloatField(initial=0, widget=forms.TextInput(attrs={'class': 'form-control','disabled':'disabled'}),label='采购金额')
    currency = forms.CharField(max_length=50,initial='',label='币种')
    exrate = forms.FloatField(initial=1,label='汇率')
    arrival_date = forms.DateField(label='到港日期')
    clearance_date = forms.DateField(label='清关日期')
    account_period = forms.IntegerField(initial=0, label='账期')
    deadline = forms.DateField(label='截止日期')
    share_cost = forms.FloatField(initial=0,widget=forms.TextInput(attrs={'class': 'form-control',}),label='均摊总成本')





