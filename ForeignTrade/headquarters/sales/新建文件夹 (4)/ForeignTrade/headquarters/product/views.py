from django.shortcuts import render,HttpResponse
from django.views import View
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from product.models import *
from django.core import serializers
from ForeignTrade.my_class import Layui
import json
# Create your views here.

# treeview(bootstrap)
# def product_type_to_json():
#     product_type = ProductType.objects.all()
#     first_type = product_type.filter(type_pid='0')
#     tree = []                  # 整个树结构
#     for f in first_type:
#         type_id = f.type_id
#         type_name= f.type_name
#         tree.append({'text': type_name, 'href':type_id ,'nodes': []})
#         next_tree = tree[-1]['nodes']
#         next_type = product_type.filter(type_pid=type_id)
#         if next_type:
#             for n in next_type:
#                 next_tree.append({'text': n.type_name, 'href': n.type_id, 'nodes': []})
#                 end_tree = next_tree[-1]['nodes']
#                 end_type = product_type.filter(type_pid=n.type_id)
#                 for e in end_type:
#                     end_tree.append({'text': e.type_name, 'href': e.type_id,})
#
#
#
#     type_tree = json.dumps(tree)
#     return type_tree


# layui tree
def product_type_to_json():
    product_type = ProductType.objects.all()
    first_type = product_type.filter(type_pid='0')
    tree = []                  # 整个树结构
    for f in first_type:
        type_id = f.type_id
        type_name= f.type_name
        tree.append({'name': type_name, 'id':type_id ,'children': []})
        next_tree = tree[-1]['children']
        next_type = product_type.filter(type_pid=type_id)
        if next_type:
            for n in next_type:
                next_tree.append({'name': n.type_name, 'id': n.type_id, 'children': []})
                end_tree = next_tree[-1]['children']
                end_type = product_type.filter(type_pid=n.type_id)
                for e in end_type:
                    end_tree.append({'name': e.type_name, 'id': e.type_id,})
    type_tree = json.dumps(tree)
    return type_tree





#获取产品信息
def get_product(request):
    product_id = request.GET.get('product_id',None)
    if product_id is None:
        return HttpResponse('no result')
    else:
        product = Product.objects.filter(product_id = product_id)
        fields = ['id','product_id','name','model','spec','eng_name','eng_spec',
                  'spanish_name','spanish_spec','mesu_unit',]
        layui = Layui(request,product,fields,1)
        data = layui.laytable_url()
    return HttpResponse(data,content_type='application/json')


class ProductView(View):
    def get(self,request,search):
        user = request.user
        if search == 'all':
            product = Product.objects.all().order_by('product_id')
        # 收到ztree类以及检索信息，则返回检索到的queryset类
        else:
            if user.language == 'Spanish':
                product = Product.objects.filter(Q(product_id__contains=search)|Q(spanish_name__contains=search)|
                                                 Q(spanish_spec__contains=search)|Q(peru_name__contains=search)|
                                                 Q(peru_spec__contains=search)|Q(mexico_name__contains=search)|
                                                 Q(mexico_spec__contains=search)|Q(type__type_name=search)).order_by('product_id')
            else:
                product = Product.objects.filter(Q(product_id__contains=search) | Q(name__contains=search) |
                                                 Q(spec__contains=search)|Q(type__type_name=search)).order_by('product_id')
        paginator = Paginator(product, 10)
        page = request.GET.get('page', '1')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'product/product.html', {'product_type': product_type_to_json(),
                                                       'product': contacts, 'page': paginator,
                                                       'user': user})


class ProductSelectView(View):
    def get(self,request):
        search = request.GET.get('search', None)
        limit = request.GET.get('limit',10)
        page = request.GET.get('page',1)
        print(request.GET)
        print(search)
        # search = search['search']
        if search is not None:
            if request.user.language == 'Spanish':
                product = Product.objects.filter(Q(product_id__contains=search) | Q(spanish_name__contains=search) |
                                                 Q(spanish_spec__contains=search) | Q(peru_name__contains=search) |
                                                 Q(peru_spec__contains=search) | Q(mexico_name__contains=search) |
                                                 Q(mexico_spec__contains=search) | Q(type__type_name=search)).order_by(
                    'product_id')
            else:
                product = Product.objects.filter(Q(product_id__contains=search) | Q(name__contains=search) |
                                                 Q(spec__contains=search) | Q(type__type_name=search)).order_by(
                    'product_id')
        else:
            product = Product.objects.all()
        length = len(product)
        page_product = Paginator(product,limit)
        try:
            data =  page_product.page(page)

        except EmptyPage:
            data = page_product.page(1)
        except PageNotAnInteger:
            data =page_product.page(1)
        except Exception as e:
            print(e)
            data = []
        products = []
        for item in data:
            product_dict = {}
            for key,value in item.__dict__.items():
                product_dict[key] = value
            product_dict.pop('_state')
            product_dict.pop('image')
            products.append(product_dict)

        my_dict = {
            "status": 0,
            "message": "",
            "total": length,
            "data": products,
        }
        data = json.dumps(my_dict)
        return HttpResponse(data, content_type='application/json')

    def post(self,request):
        product_id = request.POST.get('product_id','')
        if not product_id:
            product =  Product.objects.get(product_id=product_id)
            data = serializers.serialize('json',product)
            return HttpResponse(data,content_type='application/json')



