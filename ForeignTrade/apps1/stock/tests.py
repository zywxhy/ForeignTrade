from django.test import TestCase
import xlrd
# Create your tests here.
def salesproduct():
    workbook = xlrd.open_workbook('D:\\Documents\\Tencent Files\\122320430\\FileRecv\\秘鲁销售合同0926最终版本.xlsx')
    sheet_names = workbook.sheet_names()

    for sheet_name in sheet_names:
        sheet2 = workbook.sheet_by_name(sheet_name)
        print(sheet_name)
        for i in range(666):
            if i > 0:
                rows = sheet2.row_values(i)
                data = {}

                print(rows[17])


def stock_save():
    workbook = xlrd.open_workbook('C:\\Users\\Administrator\\Desktop\\20180930秘鲁 期初库存.xlsx')
    sheet_names = workbook.sheet_names()
    from product.models import Product
    from datetime import date
    from stock.models import StockProduct,Stock
    stock_id = Stock.objects.get(name='秘鲁仓库')
    for sheet_name in sheet_names:
        sheet2 = workbook.sheet_by_name(sheet_name)
        print(sheet_name)
        for i in range(245):
            if i > 0:
                rows = sheet2.row_values(i)
                product_id = rows[1]
                try:
                    id = Product.objects.get(product_id=product_id).id
                except Exception as e:
                    print(i)
                    continue
                my_dict = {
                    'stock_id':1,
                    'product_id': id,
                    'count' :rows[2],
                    'bad_count': rows[3],
		    'recent_date':date.today(),
                }
                StockProduct.objects.create(**my_dict)