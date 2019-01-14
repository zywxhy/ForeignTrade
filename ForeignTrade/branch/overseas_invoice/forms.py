from django import forms


class OverseasInvoicePlanForm(forms.Form):
    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        branch_sales_num = request.GET.get('branch_sales_num','')
        self.fields['branch_sales'].initial = branch_sales_num


    branch_sales = forms.CharField(label='销售合同号')
    overseas_invoice_num = forms.CharField(max_length=50, label='出库单号', help_text='出库单号',widget=forms.TextInput(attrs={'class': 'form-control'}))
    invoice_date = forms.DateField(label='出库日期', help_text='出库日期',widget=forms.TextInput(attrs={'class': 'form-control'}))
    maker = forms.CharField(max_length=30, label='经办人', help_text='经办人',widget=forms.TextInput(attrs={'class': 'form-control'}))
    remark = forms.CharField(max_length=300, label='备注', help_text='备注',widget=forms.TextInput(attrs={'class': 'form-control'}))
    shipping_method = forms.CharField(max_length=300, label='运输方式', help_text='运输方式',widget=forms.TextInput(attrs={'class': 'form-control'}))


