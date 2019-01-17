from django.shortcuts import render,render_to_response,HttpResponse,HttpResponseRedirect,redirect,reverse
from users.forms import *
from users.models import *
from django import forms
from django.views import View
from django.contrib.auth import authenticate,login,logout
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.core import serializers
from product.models import Product
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json

from django.utils.translation import ugettext as _
# Create your views here.
# 测试留用
def A(request):
    formset = TicketFormSet()
    print(request.GET)
    print(request.content_params)
    if request.content_params:
        print(json.loads(request.content_params))
    aaaa = _('password')
    return render(request,'test/test.html',locals())



# Mix类,实现登录验证功能
class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request)



# 重复获取验证码
def refresh_captcha(request):
    new_hashkey = CaptchaStore.generate_key()
    new_imgage_url = captcha_image_url(new_hashkey)
    data = {'new_hashkey':new_hashkey,'new_imgage_url':new_imgage_url }
    json_data = json.dumps(data)
    return HttpResponse(json_data,content_type='json/applications')

# 登录
class LoginView(View):
    def get(self,request):
        form = LoginForm()
        hashkey = CaptchaStore.generate_key()
        imgage_url = captcha_image_url(hashkey)
        return render(request,'registration/login.html',locals())

    def post(self,request):
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if form.is_valid() and user is not None:
            print('authenticate success')
            login(request, user)
            print('login success')
            request.session['member_id'] = user.id
            print(user.id)
            request.session.set_expiry(0)
            return redirect(reverse('home'))
                #return redirect(reverse('home'))
        else:
            hashkey = CaptchaStore.generate_key()
            imgage_url = captcha_image_url(hashkey)
            error_msg = 'username and password does not match'
            return render(request,'registration/login.html',{'hashkey':hashkey,
                                                                  'imgage_url':imgage_url,
                                                                  'error':error_msg,
                                                                  'form':form})


class LoginoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        return redirect(reverse('login'))


class HomeView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request, 'home/home.html',{})


class FormView(View):
    def get(self,request):
        form1 = PersonForm()
        formset1 = TicketFormSet()
        return render(request, 'test/test.html', locals())

    def post(self,request):
        form1 = PersonForm(request.POST)
        if form1.is_valid():
            print(form1.cleaned_data)
            u = Person.objects.create(**form1.cleaned_data)

        formset = TicketFormSet(request.POST)
        for form in formset:
            if form.is_valid():
                pass
            else:
                return HttpResponse(form.errors)

        for form in formset:
            Ticket.objects.create(**form.cleaned_data)

        return HttpResponse('OK')





