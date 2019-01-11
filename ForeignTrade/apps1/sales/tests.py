from django.test import TestCase

# Create your tests here.
import xlrd
import xlwt
from collections import Counter
from datetime import date,datetime
from client.models import Client
from users.models import MyUser
from sales.models import SalesContract,SalesProduct
from product.models import Product

def Sale():
    workbook = xlrd.open_workbook('C:\\Users\\Administrator\\Desktop\\秘鲁销售合同0926最终版本.xlsx')
    sheet_names= workbook.sheet_names()



    for sheet_name in sheet_names:
        sheet2 = workbook.sheet_by_name(sheet_name)
        print(sheet_name)
        for i in range(666):
            if i > 0:
                rows = sheet2.row_values(i)
                data = {}

                data1 = xlrd.xldate_as_tuple(sheet2.cell(i, 1).value, 0)
                time_list = data1.__str__().replace('(','').replace(')','').split(',')
                date_tuple =(int(time_list[0]),int(time_list[1]),int(time_list[2]))
                data['date']= date(int(time_list[0]),int(time_list[1]),int(time_list[2]))
                try:
                    client = Client.objects.get(name=rows[2]).id
                except Exception as e: 
                    print(e)
                    print(len(rows[2]))
                    SalesContract.objects.all().delete()
                    break
                data['client_id'] = client
                try:   
                    data['sales_num'] = str(int(rows[4]))
                except:
                    data['sales_num'] = str((rows[4]))
                try:
                    data['salesman_id'] = MyUser.objects.get(first_name=rows[3]).id
                except Exception as e: 
                    print(e)
                    print(rows[3])  
                    print(i)
                    print(len(rows[3]))
                try:
                    SalesContract.objects.create(**data)
                except Exception as e:
                    
                    continue



def salesproduct():
    workbook = xlrd.open_workbook('C:\\Users\\Administrator\\Desktop\\秘鲁销售合同0926最终版本.xlsx')
    sheet_names = workbook.sheet_names()

    for sheet_name in sheet_names:
        sheet2 = workbook.sheet_by_name(sheet_name)
        print(sheet_name)
        for i in range(666):
            if i > 0:
                rows = sheet2.row_values(i)
                data = {}

                try:
                    product = Product.objects.get(product_id=rows[5]).id
                except Exception as e:
                    print(e)
                    print(rows[5])
                    print(i)
                    break
                data['product_id'] = product
                try:
                    data['sales_id'] = SalesContract.objects.get(sales_num = str(int(rows[4]))).id
                except:
                    data['sales_id'] = SalesContract.objects.get(sales_num = str(rows[4])).id
                print(rows[11])
                data['count'] = int(rows[9])
                data['unit_price'] = float(rows[17])
                data['amount'] = float(rows[18])
                if rows[19] == '':
                    data['discount'] = 0
                else:
                    data['discount'] = rows[19]
                
                data['receivable_amount'] = float(rows[20])
               
                try:
                    SalesProduct.objects.create(**data)
                except Exception as e:
                    print(e)
                    print(i)
                    continue



