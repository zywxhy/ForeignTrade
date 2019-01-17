#此类用于分割需要的字段
from product.models import *
from django.shortcuts import render,render_to_response,HttpResponse,HttpResponseRedirect,redirect,reverse
from datetime import date
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import json

from django.db.models.fields.files import FieldFile
from django.db.models.base import Model
from django.views import View









class DataSplit:
    def __init__(self,json_data,fields,my_model):
        self.json_data = json_data         #要切割的字典
        self.model = my_model              #要添加的model
        self.fields = fields               #需要的字段

    def data_split(self,contract_dict,):       #关联的外键,用dict形式
        if self.json_data is None:
            return None
        data = json.loads(self.json_data)
        try:
            for item in data:
                new_item = {}
                for key,value in item.items():
                    if not self.fields.__contains__(key):
                        pass
                    else:
                        new_item[key] = value
                if item.__contains__('product__product_id'):
                     product__product_id = item.get('product__product_id')
                     product_id = Product.objects.get(product_id = product__product_id).id
                     new_item['product_id'] = product_id
                print(new_item)
                self.model.objects.create(**contract_dict,**new_item)
            return True

        except Exception as e:
            print(e)
            return False


class ContractOperations:
    def __init__(self,contract,form,error_index=None,sub_split1=None,sub_split2=None):
        self.contract = contract
        self.form = form
        self.error_index = error_index
        self.sub_split1 = sub_split1
        self.sub_split2 = sub_split2

    def contract_add(self,foreign_pk,extra=None,pop_list=None):
        if self.form.is_valid():
            print(self.form.cleaned_data)
            try:
                if pop_list is not None:
                    for pop_item in pop_list:
                        self.form.cleaned_data.pop(pop_item)
                if extra is not None:
                    print(self.form.cleaned_data)
                    contract = self.contract.objects.create(**self.form.cleaned_data,**extra)
                else:
                    contract = self.contract.objects.create(**self.form.cleaned_data)
                if self.sub_split1:
                    if not self.sub_split1.data_split({foreign_pk:contract.id}):
                        self.error_index = 3
                        return False
                if self.sub_split2:
                    if not self.sub_split2.data_split({foreign_pk:contract.id}):
                        self.error_index = 4
                        return False
                self.error_index = 0
                return contract
            except Exception as e:
                print(e)
                self.error_index = 1
                return False
        else:
            print(self.form.errors)
            self.error_index = 2
            return False

    def contract_modify(self,pk,foreign_pk):
        contract = self.contract.objects.filter(id=pk)
        if self.form.is_valid():
            try:
                contract.update(**self.form.cleaned_data)
                self.sub_split1.model.filter({foreign_pk:pk}).delete()
                self.sub_split2.model.filter({foreign_pk:pk}).delete()
                if self.sub_split1:
                    if not self.sub_split1.data_split({foreign_pk:pk}):
                        self.error_index = 3
                        return False
                if self.sub_split2:
                    if not self.sub_split2.data_split({foreign_pk:pk}):
                        self.error_index = 4
                        return False
                self.error_index = 0
                return False
            except Exception as e:
                print(e)
                self.error_index = 1
                return False
        else:
            print(self.form.errors)
            self.error_index = 2
            return False



class ContractDetail:
    def __init__(self):
        pass









#Layui类 返回Layui所需的格式
class Layui:
    def __init__(self,request,model,fields,count,page=None,limit=10,):
        self.model = model
        self.fields = fields
        self.count = count
        self.request = request
        self.page = page
        self.limit = limit
        # self.field = self.request.GET.get('field', None)
        # self.order = self.request.GET.get('order', None)
        # if self.field is not None:
        #     self.laytable_order()
    def laytable_data(self,is_json=None):

        my_data = []
        if self.page is not None:                         #如果有page
            paginator = Paginator(self.model,self.limit)    #建立分页
            try:
                self.model = paginator.page(self.page)
            except EmptyPage:
                self.model = []
            except PageNotAnInteger:
                self.model = paginator.page(1)              #取得该页数据
        for item in self.model:
            my_dict = {}
            for field in self.fields:                     #遍历字段列表
                field_list = field.split('__')            #切割__拿到关联表的句柄，循环下去
                result = item
                for i in field_list:
                    result = getattr(result,i)
                    if isinstance(result,date):
                        result = str(result)
                    my_dict[field] = result                #将结果加入字典

            my_data.append(my_dict)                       #该行数据加入列表中
            if is_json is not None:
                return json.dumps(my_data)
        return my_data


    def laytable_url(self):
        my_data = self.laytable_data()       #这里我们需要非json格式的数据
        new_data = {
            "code": 0,
            "msg": "",
            "count": self.count,
            "data": my_data,
        }
        return json.dumps(new_data)       #返回json格式的数据




    # def laytable_order(self):
    #     if self.order == 'desc':
    #         self.model = self.model.order_by(self.field).reverse()
    #     else:
    #         self.model = self.model.order_by(self.field)




# 0 未审核 1已审核 2已退回（或反审）
def review(model,status,callback,*args,**kwargs):
    model.status = status
    model.save()
    callback(*args,**kwargs)
    return




class ModelDetail:
    def __init__(self,form,sub_model_list):
        self.form = form
        self.sub_model_list = sub_model_list







