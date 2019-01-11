from django.test import TestCase

# Create your tests here.
import xlrd
import xlwt
from collections import Counter
from product.models import ProductType,Product
def k():
    workbook = xlrd.open_workbook('E:\\0925 产品信息确认00.xlsx')

    sheet_names= workbook.sheet_names()

    i = 0

    counter = Counter([])
    for sheet_name in sheet_names:
        sheet2 = workbook.sheet_by_name(sheet_name)
        print(sheet_name)
        # while True:
        #     if i > 0 and i<95:
        #         rows = sheet2.row_values(i) # 获取第1行内容
        #         # cols = sheet2.col_values(1) # 获取第1列内容
        #
        #         print(rows)
        #     i += 1
        for i in range(595):
            if i>0:
                rows = sheet2.row_values(i)
                counter.update([str(int(rows[0]))+':'+rows[1]])
    print(counter)




    #大类录入
    for key,value in counter.items():
        i = key.split(':')
        ProductType.objects.create(type_pid=0,type_id=i[0],type_name=i[1],is_parent=True)


    # 小类录入
    # counter = Counter([])
    # for sheet_name in sheet_names:
    #     sheet2 = workbook.sheet_by_name(sheet_name)
    #     print(sheet_name)
    #     # while True:
    #     #     if i > 0 and i<95:
    #     #         rows = sheet2.row_values(i) # 获取第1行内容
    #     #         # cols = sheet2.col_values(1) # 获取第1列内容
    #     #
    #     #         print(rows)
    #     #     i += 1
    #     for i in range(595):
    #         if i>0:
    #             rows = sheet2.row_values(i)
    #             first_type = str(int(rows[1]))
    #
    #             second_type = str(int(rows[3]))
    #             second_name = rows[2]
    #             counter.update([first_type +'0'+ second_type + ':' + second_type+':'+second_name])
    #
    #
    #
    # # 小类
    # for key,value in counter.items():
    #     i = key.split(':')
    #     ProductType.objects.create(type_pid=i[0][0:3],type_id=i[0],type_name=i[2],is_parent=False)


# 种类录入
def M():
    workbook = xlrd.open_workbook('E:\\0925 产品信息确认00.xlsx')

    sheet_names= workbook.sheet_names()

    i = 0

    counter = Counter([])
    for sheet_name in sheet_names:
        sheet2 = workbook.sheet_by_name(sheet_name)
        print(sheet_name)
        # while True:
        #     if i > 0 and i<95:
        #         rows = sheet2.row_values(i) # 获取第1行内容
        #         # cols = sheet2.col_values(1) # 获取第1列内容
        #
        #         print(rows)
        #     i += 1
        for i in range(596):
            if i>0:
                rows = sheet2.row_values(i)
                counter.update([str(int(rows[2]))+':'+rows[3]])
    print(counter)




    #中 类录入
    for key,value in counter.items():
        i = key.split(':')
        ProductType.objects.create(type_pid=i[0][:3],type_id=i[0],type_name=i[1],is_parent=True)





def S():
    workbook = xlrd.open_workbook('E:\\0925 产品信息确认00.xlsx')

    sheet_names= workbook.sheet_names()

    # 小类录入
    counter = Counter([])
    for sheet_name in sheet_names:
        sheet2 = workbook.sheet_by_name(sheet_name)
        print(sheet_name)
        # while True:
        #     if i > 0 and i<95:
        #         rows = sheet2.row_values(i) # 获取第1行内容
        #         # cols = sheet2.col_values(1) # 获取第1列内容
        #
        #         print(rows)
        #     i += 1
        for i in range(596):
            if i>0:
                rows = sheet2.row_values(i)


                first_type = str(int(rows[2]))
                second_type = '0'+str(int(rows[4]))
                second_name = rows[5]
                counter.update([ first_type+second_type+':'+second_name])


    print(counter)
    # 小类
    for key,value in counter.items():
        i = key.split(':')
        ProductType.objects.create(type_pid=i[0][0:5],type_id=i[0],type_name=i[1],is_parent=False)



def C():
    workbook = xlrd.open_workbook('E:\\桌面文件\\0925 产品信息确认.xlsx')

    sheet_names= workbook.sheet_names()

    i = 0

    counter = Counter([])
    for sheet_name in sheet_names:
        sheet2 = workbook.sheet_by_name(sheet_name)
        print(sheet_name)
        # while True:
        #     if i > 0 and i<95:
        #         rows = sheet2.row_values(i) # 获取第1行内容
        #         # cols = sheet2.col_values(1) # 获取第1列内容
        #
        #         print(rows)
        #     i += 1
        for i in range(595):
            if i>0:
                rows = sheet2.row_values(i)
                counter.update([str(rows[0])+':'+str(int(rows[1]))])


    key1=[]
    for key,value in counter.items():
        new_key = key.split(':')
        key1.append(new_key)
    index = 0
    length = len(key1)
    error = []
    for i in key1:
        i_id = i[1]
        i_name = i[0]
        for j in key1[index+1:]:
            j_id = j[1]
            j_name = j[0]
            if i_id == j_id:
                error.append(i_id+i_name+'error'+j_name)
        index +=1


    print(error)



def Check():
    workbook = xlrd.open_workbook('E:\\桌面文件\\0925 产品信息确认.xlsx')

    sheet_names= workbook.sheet_names()
    i = 0

    counter = Counter([])
    for sheet_name in sheet_names:
        sheet2 = workbook.sheet_by_name(sheet_name)
        print(sheet_name)
         # while True:
            #     if i > 0 and i<95:
            #         rows = sheet2.row_values(i) # 获取第1行内容
            #         # cols = sheet2.col_values(1) # 获取第1列内容
            #
            #         print(rows)
            #     i += 1
        for i in range(595):
             if i>0:
                 rows = sheet2.row_values(i)
                 counter.update([str(rows[0])+':'+str(int(rows[1]))])


    key1=[]
    for key,value in counter.items():
         new_key = key.split(':')
         key1.append(new_key)
    index = 0
    length = len(key1)
    error = []
    for i in key1:
        i_id = i[1][0:3]
        i_name = i[0]
        for j in key1[index+1:]:
            j_id = j[1]
            j_name = j[0]
            if i_name == j_name:
                error.append(i_id+':::'+j_id)
        index +=1


    print(set(error))




def P():

        workbook = xlrd.open_workbook('E:\\0925 产品信息确认00.xlsx')

        sheet_names = workbook.sheet_names()


        for sheet_name in sheet_names:
            sheet2 = workbook.sheet_by_name(sheet_name)
            print(sheet_name)
            # while True:
            #     if i > 0 and i<95:
            #         rows = sheet2.row_values(i) # 获取第1行内容
            #         # cols = sheet2.col_values(1) # 获取第1列内容
            #
            #         print(rows)
            #     i += 1
            for i in range(596):
                if i > 0:
                    rows = sheet2.row_values(i)
                    data = {}
                    data['product_id'] = str(int(rows[8]))
                    data['name'] = rows[10]
                    data['model'] = rows[6]
                    data['eng_name'] = rows[9]
                    data['spec'] = rows[11]
                    data['eng_spec'] = rows[12]
                    data['old_id'] = rows[13]
                    first_type = str(int(rows[2]))
                    second_type = '0' + str(int(rows[4]))
                    id = ProductType.objects.get(type_id=first_type+second_type).id
                    data['type_id'] = id
                    Product.objects.create(**data)



def B():
    workbook = xlrd.open_workbook('D:\\Documents\\Tencent Files\\122320430\\FileRecv\\新建编码0927.xlsx')

    sheet_names= workbook.sheet_names()




    for sheet_name in sheet_names:
        sheet2 = workbook.sheet_by_name(sheet_name)
        print(sheet_name)
        # while True:
        #     if i > 0 and i<95:
        #         rows = sheet2.row_values(i) # 获取第1行内容
        #         # cols = sheet2.col_values(1) # 获取第1列内容
        #
        #         print(rows)
        #     i += 1
        for i in range(5):
            if i>0:
                rows = sheet2.row_values(i)
                data = (rows[8][:8]+':'+rows[8]+':'+rows[6]+':'+rows[10]+':'+rows[11]+':'+rows[9]+':'+rows[12])
                data2 = data.split(':')
                product_type = ProductType.objects.get(type_id=data2[0]).id
                Product.objects.create(product_id=data2[1],model=data2[2],name=data2[3],spec=data2[4],eng_name=data2[5],eng_spec=data2[6])



def GAI():
    workbook = xlrd.open_workbook('D:\\Documents\\Tencent Files\\122320430\\FileRecv\\20181015 改型号.xlsx')
    sheet_names = workbook.sheet_names()

    for sheet_name in sheet_names:
        sheet2 = workbook.sheet_by_name(sheet_name)
        print(sheet_name)
        # while True:
        #     if i > 0 and i<95:
        #         rows = sheet2.row_values(i) # 获取第1行内容
        #         # cols = sheet2.col_values(1) # 获取第1列内容
        #
        #         print(rows)
        #     i += 1
        for i in range(48):
            rows = sheet2.row_values(i)
            product_id = rows[3]
            product = Product.objects.get(product_id =product_id)
            if rows[7] == 'delete':
                product.delete()
                continue
            product.name = rows[4]
            product.spec = rows[5]
            product.eng_name = rows[6]
            product.model = rows[7]
            if rows[9]:
                product.eng_spec = rows[9]
            product.save()



a=['SAMPLE', '', '', '1000101000001', 'GJYXFCH-2B样品',
   'GJYXFCH-2B，吊线7*0.35钢绞线 （满足80m跨距）样品各200m', 'SAMPLE', 'FTTH SAMPLE2', '更新', '']
