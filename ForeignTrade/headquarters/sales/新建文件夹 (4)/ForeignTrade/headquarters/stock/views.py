from django.shortcuts import render,HttpResponse
from django.views import View
from stock.models import StockProduct,StockRecord,Stock
from sales.models import SalesProduct,time_to_str
from purchase.models import PurchaseProduct,PurchaseContract
from invoice.models import Invoice,InvoiceProduct
from invoice.forms import InvoiceAddForm
from storage.models import Storage,StorageProduct
from storage.forms import StorageAddForm
from product.models import Product
from client.models import Client
from ForeignTrade.my_class import DataSplit,Layui
import json
# Create your views here.

def get_stock_product(request):
    stock = Stock.objects.all()
    return render(request,'stock/stock_product.html',locals())




class StockView(View):
    def get(self,request):
        user = request.user
        stock_id = request.GET.get('stock_id')
        try:
            stock = Stock.objects.get(id=stock_id)

            if user.permission_level>=3:
                #StockProduct().mrp(stock_id)
                stock_product = stock.stockproduct_set.all()
            else:
                if user.company_id == stock.id:
                    stock_product = stock.stockproduct_set.all()
                else:
                    stock_product = []
        except:
            stock_product = []
        count = len(stock_product)
        fields = ['product__model', 'product__name', 'product__spec', 'recent_date', 'count']
        layui = Layui(request, stock_product, fields, count)
        json_data = json.dumps(layui.laytable_url())

        return HttpResponse(json_data,content_type='application/json')


    def post(self, request):
         pass


class StockRecordView(View):
    def get(self,request):
        user = request.user
        stock_id = request.GET.get('stock_id')
        try:
            stock = Stock.objects.get(id=stock_id)
        except:
            return HttpResponse('404 Error')
        if user.permission_level>=3:
            #StockProduct().mrp(stock_id)
            stock_product = stock.stockrecord_set.all()
        else:
            if user.company_id == stock.id:
                stock_product = stock.stockrecord_set.all()
            else:
                stock_product = []
        return render(request, 'stock/stock_product.html', locals())


    def post(self, request):
         pass



class StockReviewView(View):
    # 审核操作

    def get(self, request):
        invoice = Invoice.objects.filter(sales__salesman__company_id=request.user.company.id, status=1)
        storage = Storage.objects.filter(purchase__buyer__company_id=request.user.company.id, status=1)
        return render(request, 'stock.stock_review.html', locals())

    def post(self,request):
        user = request.user
        reviewer = user.first_name
        type = request.POST.get('type')
        odd_num = request.POST.get('odd_num')
        result = request.POST.get('result')
        stock_id = Stock.objects.get(country=user.country).stock_id
        if not user.is_warehouse_reviewer:
            return HttpResponse('no permission')
        if type == 'storage':
            if result == 'N':
                storage = Storage.objects.get(Storage_num=odd_num)
                storage.status = 2
                storage.save()
            elif result == 'Y':
                if Storage.objects.get(Storage_num=odd_num).status != 0:
                    return HttpResponse('请勿重复入库')
                else:
                    storage = Storage.objects.get(storage_num=odd_num)
                    if stock_in(odd_num, reviewer, stock_id):
                        storage.status = 1
                        storage.save()
                        return HttpResponse('入库成功')
                    else:
                        return HttpResponse('入库失败，请联系管理员')
        else:
            if result == 'N':
                invoice = Invoice.objects.get(invoice_num=odd_num)
                invoice.status = 2
                invoice.save()
            elif request == 'Y':
                if Invoice.objects.get(invoice_num=odd_num).status != 0:
                    return HttpResponse('请勿重复出库')
                else:
                    invoice = Invoice.objects.get(invoice_num=odd_num)
                    client = Client.objects.get(name=invoice.client)

                    if stock_out(odd_num, reviewer, stock_id):
                        if client.is_branch:
                            invoice.status = 1
                            invoice.save()
                            if purchaseAddOverseas(client, invoice):
                                return HttpResponse('出库成功,海外采购单已自动生成，请核对')
                            else:
                                return HttpResponse('出库成功,海外采购单生成失败，请联系管理员')
                        else:
                            invoice.status = 1
                            invoice.save()
                            return HttpResponse('出库成功')
                    else:
                        return HttpResponse('出库失败，请联系管理员')


# 出库单审核通过后，出库操作，并写入出入库记录中
def stock_out(num,reviewer,stock_id):
    order = Invoice.objects.get(invoice_num=num)  # 当前出库单
    product_list = SalesProduct.objects.filter(invoice_num_id=num)  # 当前出库单产品
    sales_order_num=order.sales_order_num   # 入库单关联的采购单号
    sales_product_list = SalesProduct.objects.all()  # 相关销售单
    record = StockRecord.objects.all() # 仓储记录表
    stock_product = StockProduct.objects.all() # 仓库产品表
    # 遍历检查（仓库数量是否满足）
    for g in product_list:
        product = stock_product.filter(product_id=g.product_id, stock_id=stock_id)  # 获取该仓库该产品
        if len(product) == 0:  # 没有该产品
            print('stock:'+stock_id+'has not the product:'+g.product_id)
            return False
        else:
            product = stock_product.get(product_id=g.product_id, stock_id=stock_id)  # 精确获取该产品
            if g.count > product.count:
                print('stock:' + stock_id + 'has not the product:' + g.product_id+'more')
                return False
    # 检查通过，出库流程
    print('check success')
    try:
        for g in product_list:
            if g.count != 0:  # 判断出库单产品不为0，进行下一项操作
                product = stock_product.get(product_id=g.product_id,stock_id=stock_id) #已经进行过检查，可以直接精准获取

                old_total_price = product.count * product.unit_price  # 仓库现有价值
                print(old_total_price)
                total_price = old_total_price - g.count * product.unit_price    #出库后剩余价值
                count = product.count - g.count    # 仓库剩余数量
                product.count = count
                product.date = order.date
                product.save()              # 数量 单价 时间保存

                record.create(reviewer=reviewer,date=order.date,stock_id=stock_id,product_id=g.product_id,name=g.name,
                              specifications=g.specifications,remark=g.remark,measurement_unit=g.measurement_unit,
                              unit_price=g.unit_price,count=g.count,in_or_out=0,order_num=num,cost_unit_price=product.unit_price)
                     #存入记录中

                if count == 0:
                    product.delete()

                item = sales_product_list.get(product_id=g.product_id,sales_order_num_id=sales_order_num)  #将出库数量填入销售单产品表中
                outbound_count = item.outbound_count # 当前已出库数量
                outbound_count += g.count            # 实际出库数量
                print(outbound_count)
                item.outbound_count = outbound_count
                item.save()             #保存
        return True
    except Exception as e:
        print(e)
        return False


#入库单审核通过后，入库操作，入库并写入出入库记录中
def stock_in(num,reviewer,stock_id):
    odd = Storage.objects.get(storage_num=num)  #当前入库单
    product_list = StorageProduct.objects.filter(storage_id=odd.id)  #当前入库单产品
    purchase_num=odd.purchase.purchase_num   # 入库单关联的采购单号
    purchase_product = PurchaseProduct.objects.all()  # 采购单
    record = StockRecord.objects.all() # 仓储记录表
    stock_product = StockProduct.objects.all() #仓库产品表
    try:
        for product in product_list:
            if product.count != 0:  # 判断不为0，进行下一项操作
                product = stock_product.filter(product_id=product.product_id,stock_id=stock_id) #!!!一定注意仓库
                if len(product) == 0: # 该产品在该仓库中没有
                    stock_product.create(product_id=product.id,unit_price=product.unit_price,date=odd.warehouse_date,count=product.count)  #创建该产品
                else:    # 该产品在该仓库中有
                    product = stock_product.get(product_id=product.product.id,stock_id=stock_id)  #精确获取该产品
                    old_total_price = product.count * product.unit_price
                    total_price = old_total_price + product.count * product.unit_price
                    count = product.count + product.count
                    unit_price = total_price/count
                    product.count = count
                    product.unit_price = unit_price
                    product.date = odd.warehouse_date
                    product.save()               #以上函数加权平均并存入仓库


                record.create(reviewer=reviewer,date=odd.warehouse_date,stock_id=stock_id,product_id=product.product.id,
                              remark=product.remark,cost_unit_price=product.unit_price,count=product.count,in_or_out=1,order_num=num)
                     #存入记录中

                item = purchase_product.get(product_id=product.product.id,purchase_num=purchase_num)  #将入库数量填入采购单产品表中
                storage_count = item.storage_count  # 当前已入库数量
                storage_count += product.count            # 实际入库数量
                print(storage_count)
                item.storage_count = storage_count
                item.save()             #保存
        return True
    except Exception as e:
        print(e)
        return False

#(返回一个dict{'product_id':'total_unit_price'}
def warehousing_cost_split(warehousing,product_cost_list,share_cost):
    warehousing_num = warehousing.warehousing_num
    product_list = StockProduct.objects.first(warehousing_num_id = warehousing_num)
    index = int(len(product_cost_list)/3)   # product_id ,other_cost_num ,other_cost_price
    print(warehousing)
    print(product_cost_list)
    volume = 0
    for product in product_list:
         volume += product.volume
    if share_cost != 0:
        share_cost_v = share_cost/volume
    else:
        share_cost_v = 0
    try:
        for i in range(1, index + 1):
            product =product_list.get(product_id=product_cost_list['product_id'],warehousing_num_id=warehousing_num)
            product.other_cost_name = product_cost_list['other_cost_name' + str(i)]
            product.other_cost_price = product_cost_list['other_cost_price' + str(i)]
            product.freight_sharing = share_cost_v * product.volume
            product.save()

        return True
    except Exception as e:
        print(e)
        return False

def purchaseAddOverseas(client,invoice):
    data = {
        'purchasing_order_num':'P'+time_to_str(),
        'country':client.country,
        'supplier':'China',
        'date' :invoice.date,
        'money_type':invoice.sales.currency,
        'exchange_rate': 1.0,
        'buyer':client.name,
    }
    try:
        purchase = PurchaseContract.objects.create(**data)
        goods_list = Invoice.objects.filter(invoice_num_id=invoice.invoice_num)
        for good in goods_list:
            PurchaseProduct.objects.create(
                purchase_id = purchase.id,
                product_id=good.id,
                remark = good.remark,
                count = good.count,
                unit_price = good.unit_price)
        return True
    except Exception as e:
        print('purchaseaddoverseasERROR:',e)
        return False