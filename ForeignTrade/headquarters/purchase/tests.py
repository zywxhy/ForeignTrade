from django.test import TestCase

# # Create your tests here.
# a = ['date',('client',['name']),('salesman',['first_name']),'sales_num',('product',['model','name','spec']),'count']
#
# k = []
# for item in a:
#     if isinstance(item,tuple):
#         for j in item[1]:
#             k.append(item[0]+'__'+j)
#     else:
#         k.append(item)
#
# print(k)
#
#
a = 'k'
b=a.split('__')
print(b)