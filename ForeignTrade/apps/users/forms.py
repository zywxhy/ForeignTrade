from captcha.fields import CaptchaField
from django import forms
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,required=True,label=_('user'),widget=forms.TextInput(attrs={'class': 'form-control'})) #给自动生成的input标签自定义class属性
    password = forms.CharField(max_length=30,required=True,label=_('password'))
    #captcha = CaptchaField(label=_('captcha'))



class PersonForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'form-inline'

    name = forms.CharField(max_length=20, required=True , label='名字')
    info = forms.CharField(max_length=20, required=True, label='信息')




class TicketForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'form-inline'

    name = forms.CharField(max_length=20, required=True, label='票名')

TicketFormSet = forms.formset_factory(TicketForm, extra=3, max_num=99)
