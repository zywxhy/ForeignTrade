from django import forms
from users.models import MyUser
from purchase.models import PurchaseContract

class StorageAddForm(forms.Form):
    def __init__(self,request,method,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if method == 'get':
            purchase = PurchaseContract.objects.get(purchase_num=request.GET['purchase_num'])
            self.fields['purchase_num'].initial = purchase.purchase_num
            self.fields['maker'].initial = request.user.first_name
        else:
            pass

        #self.fields['']


    storage_num = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control',}), label='入库单号')
    purchase_num = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','disabled':'disabled'}),label='采购单号')
    maker = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','disabled':'disabled'}),label='制单人')
    #reviewer = forms.ModelChoiceField(queryset=MyUser.objects.all(),widget=forms.Select(attrs={'class': 'form-control',}),label='审核人')
    storage_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control datepicker',}),label='入库日期')

    #arrival_date = forms.DateField(label='到港日期')
    #clearance_date = forms.DateField(label='清关日期')


    #share_cost = forms.FloatField(initial=0,widget=forms.TextInput(attrs={'class': 'form-control',}),label='均摊总成本')
    remark = forms.CharField(max_length=300, initial='', label='备注', required=False,widget=forms.Textarea(attrs={'class': 'form-control', }))




