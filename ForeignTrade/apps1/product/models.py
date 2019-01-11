from django.db import models

# Create your models here.
class ProductType(models.Model):
    type_name = models.CharField(max_length=50,verbose_name='产品类名')
    type_id = models.CharField(max_length=20,unique=True,verbose_name='类ID')
    type_pid = models.CharField(max_length=20,default='0',verbose_name='父类ID')
    is_parent = models.BooleanField(verbose_name='是否还有子类')

    class Meta:
        verbose_name = '产品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type_name


class Product(models.Model):
    type = models.ForeignKey(ProductType,on_delete=models.CASCADE,verbose_name='产品类别')
    main_type = models.CharField(max_length=50,default='',verbose_name='产品大类')
    index = models.IntegerField(default=1,verbose_name='流水号')
    product_id = models.CharField(max_length=20,unique=True,verbose_name='产品ID')
    old_id = models.CharField(max_length=30, verbose_name='原产品ID')
    image = models.ImageField(upload_to='images/%Y/%m',verbose_name='产品图片')
    name = models.CharField(max_length=200, verbose_name='产品名称')
    model = models.CharField(max_length=15,verbose_name='产品型号')
    spec = models.CharField(max_length=200,verbose_name='产品规格')
    eng_name = models.CharField(max_length=200, verbose_name='产品型号(英语)',default='')
    eng_spec = models.CharField(max_length=200, verbose_name='产品规格(英语)',default='')
    spanish_name = models.CharField(max_length=200,verbose_name='产品型号(西班牙语)',default='')
    spanish_spec = models.CharField(max_length=200,verbose_name='产品规格(西班牙语)',default='')
    mexico_name = models.CharField(max_length=200,verbose_name='产品型号(墨西哥)',default='')
    mexico_spec = models.CharField(max_length=200,verbose_name='产品规格(墨西哥)',default='')
    peru_name = models.CharField(max_length=200, verbose_name='产品型号(秘鲁)',default='')
    peru_spec = models.CharField(max_length=200, verbose_name='产品规格(秘鲁)',default='')
    mesu_unit = models.CharField(max_length=20,verbose_name='计量单位')
    volume = models.FloatField(default=0,verbose_name='单位体积')
    barcode =  models.CharField(max_length=50,default='',verbose_name='条形码')
    customs_code = models.CharField(max_length=50,default='',verbose_name='海关代码')
    carton_size = models.FloatField(default=0,verbose_name='外箱体积')
    carton_weight = models.FloatField(default=0,verbose_name='外箱毛重')
    main_supplier = models.CharField(max_length=50, default='',verbose_name='主供应商')
    cost = models.FloatField(default=0.00,verbose_name='成本(RMB)')

    class Meta:
        verbose_name = '产品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.product_id+':'+self.name+'('+self.spec+')'



