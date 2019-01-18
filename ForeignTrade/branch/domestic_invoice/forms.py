from django import forms
from.models import DomesticInvoice

class DomesticInvoiceModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('forms',self.initial)
        if not self.initial:
            self.fields['invoice_date'].initial = ''
            self.fields['estimated_date'].initial = ''
    class Meta:
        model = DomesticInvoice
        fields = ['company',
                  'domestic_invoice_num',
                  'invoice_date',
                  'estimated_date',
                  'method',
                  'freight',
                  'address',
                  'remark',
                  'bill',
                  'total_amount'
                  ]



        widgets = {
            'company': forms.Select(attrs={'class': 'form-control','autocomplete':"off"}),
            'domestic_invoice_num': forms.TextInput(attrs={'class': 'form-control','autocomplete':"off"}),
            'invoice_date': forms.TextInput(attrs={'class': 'form-control','autocomplete':"off"}),
            'estimated_date': forms.TextInput(attrs={'class': 'form-control ','autocomplete':"off"}),
            'method': forms.Select(choices=(('海运','海运'),('空运','空运')),attrs={'class': 'form-control','autocomplete':"off"}),
            'freight': forms.TextInput(attrs={'class': 'form-control changeable','autocomplete':"off"}),
            'address': forms.TextInput(attrs={'class': 'form-control','autocomplete':"off"}),
            'remark': forms.Textarea(attrs={'class': 'form-control','width':"100%",'autocomplete':"off"}),
            'bill': forms.TextInput(attrs={'class': 'form-control','autocomplete':"off"}),
            'total_amount': forms.TextInput(attrs={'class': 'form-control','autocomplete':"off","disabled":"true"}),
        }

