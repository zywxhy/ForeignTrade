from django.shortcuts import render
from django.views import View
from django.db.models import Q
from users.models import MyUser
from client.models import Client
# Create your views here.
class ClientView(View):
    def get(self,request):
        user = request.user
        client = Client.objects.filter(salesman = user)
        return render(request,'client/client.html',locals())

    def post(self,request):
        pass




class ClientSelectView(View):
    def get(self,request):
        user = request.user
        client = Client.objects.filter(salesman = user)
        return render(request, 'client/client_select.html', locals())