from django import forms
from branch_sales.models import BranchSalesContract
from branch_stock.models import BranchStock

class OverseasInvoicePlanForm(forms.Form):
    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        branch_sales = request.GET.get('branch_sales','')
        sales_num = BranchSalesContract.objects.get(id=branch_sales).sales_num
        self.fields['branch_sales'].initial = sales_num


    branch_sales = forms.CharField(label='销售合同号',widget=forms.TextInput(attrs={'class': 'form-control'}))
    overseas_invoice_num = forms.CharField(max_length=50, label='出库单号', help_text='出库单号',widget=forms.TextInput(attrs={'class': 'form-control'}))
    invoice_date = forms.DateField(label='出库日期', help_text='出库日期',widget=forms.TextInput(attrs={'class': 'form-control datetimepicker'}))
    maker = forms.CharField(max_length=30, label='经办人', help_text='经办人',widget=forms.TextInput(attrs={'class': 'form-control'}))
    remark = forms.CharField(max_length=300, label='备注', help_text='备注',widget=forms.TextInput(attrs={'class': 'form-control'}))
    shipping_method = forms.CharField(max_length=300, label='运输方式', help_text='运输方式',widget=forms.TextInput(attrs={'class': 'form-control'}))
    branch_stock = forms.ModelChoiceField(BranchStock.objects.all(), label='仓库',widget=forms.Select(attrs={'class': 'form-control'}))

