from django import forms
from sales.models import SalesContract


class InvoiceAddForm(forms.Form):
    def __init__(self,request,method,*args,**kwargs):
        super().__init__(*args, **kwargs)

        if method == 'get':
            sales_num = request.GET.get('sales_num', '')
            sales = SalesContract.objects.get(sales_num = sales_num)
            self.fields['sales_num'].initial = sales_num
            self.fields['invoice_num'].initial = 'I' + sales_num[1:] + '-' + str(sales.invoice_index)
        else:
            pass


        self.fields['maker'].initial = request.user.first_name

    invoice_num = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
                                label='出库编号', )

    sales_num = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
                            label='合同编号')
    maker = forms.CharField(max_length=20, initial='', widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
                            label='制单人')
    invoice_date = forms.DateField(label='出库日期', widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    manifest_num = forms.CharField(max_length=30, initial='', label='快递单号',
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact = forms.CharField(max_length=100, initial='', label='联系方式',
                                       widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='地址')
    ship_method = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                    choices=(('空运','空运'),('海运','海运'),('快递','快递')),label='运输方式')


