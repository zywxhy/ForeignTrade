from django import forms
from .models import BranchWarehousing
from branch_stock.models import BranchStock
from domestic_invoice.models import DomesticInvoice


class BranchWarehousingModelForm(forms.Form):
    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        domestic_invoice_id = request.GET.get('domestic_invoice','')
        odd_num = ''
        if domestic_invoice_id:
            odd_num = DomesticInvoice.objects.get(id=domestic_invoice_id).domestic_invoice_num
        self.fields['domestic_invoice'].initial = odd_num
        if self.initial:
            domestic_invoice = self.initial['domestic_invoice']
            self.initial['domestic_invoice'] = domestic_invoice.domestic_invoice_num
            #self.fields['branch_stock'].queryset = BranchStock.objects.filter(company_id=request.user.company_id)


    warehousing_num = forms.CharField(max_length=20, initial='', label='入库单号',widget=forms.TextInput(attrs={'class': 'form-control'}))
    domestic_invoice = forms.CharField(label='国内发货单',widget=forms.TextInput(attrs={'class': 'form-control'}))
    branch_stock = forms.ModelChoiceField(queryset=BranchStock.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}))
    warehousing_date = forms.DateField(initial='', label='入库时间',widget=forms.TextInput(attrs={'class': 'form-control datepicker','autocomplete':"off"}) )
    remark = forms.CharField(initial='', max_length=500, label='备注',widget=forms.TextInput(attrs={'class': 'form-control'}))


