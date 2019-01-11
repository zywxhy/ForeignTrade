from django.test import TestCase
import xlrd
from datetime import date
from supplier.models import Supplier,SupplierContacts
# Create your tests here.
def S():
    workbook = xlrd.open_workbook('E:\\桌面文件\\供应商信息20181011--.xlsx')

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
        fields1 = ['','name','area','address','eco_nature','bank_account','bank','duty_para','telephone',
                  'fax','postalcode',]
        fields2 = ['name','','position','phone','telephone','fax','email',]  #11
        fields3 = ['name','phone','position',]  #18
        for i in range(83):
            if i>0:
                rows = sheet2.row_values(i)
                data1 = {'inputting_date':date.today()}
                for i in range(len(fields1)):
                    if fields1[i] and rows[i]:
                        data1[fields1[i]] = rows[i]

                supplier = Supplier.objects.create(**data1)

                i = 11
                data2 = {'master_contact':True,'supplier_id':supplier.id}
                for item in fields2:
                    if item and rows[i]:
                        data2[item] = rows[i]
                    i+=1

                contact1 = SupplierContacts.objects.create(**data2)

                if rows[18]:
                    data3 = {'supplier_id':supplier.id}
                    i = 18
                    for item in fields3:
                        if item and rows[i]:
                            data3[item] = rows[i]
                        i += 1
                    contact2 = SupplierContacts.objects.create(**data3)



