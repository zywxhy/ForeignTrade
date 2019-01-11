# Generated by Django 2.1.1 on 2018-09-26 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='model',
            field=models.CharField(default='', max_length=200, verbose_name='产品型号'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='old_id',
            field=models.CharField(default='', max_length=30, verbose_name='原产品ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.CharField(default='', max_length=50, verbose_name='条形码'),
        ),
        migrations.AlterField(
            model_name='product',
            name='customs_code',
            field=models.CharField(default='', max_length=50, verbose_name='海关代码'),
        ),
        migrations.AlterField(
            model_name='product',
            name='eng_name',
            field=models.CharField(default='', max_length=200, verbose_name='产品型号(英语)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='eng_spec',
            field=models.CharField(default='', max_length=200, verbose_name='产品规格(英语)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='mexico_name',
            field=models.CharField(default='', max_length=200, verbose_name='产品型号(墨西哥)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='mexico_spec',
            field=models.CharField(default='', max_length=200, verbose_name='产品规格(墨西哥)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200, verbose_name='产品名称'),
        ),
        migrations.AlterField(
            model_name='product',
            name='peru_name',
            field=models.CharField(default='', max_length=200, verbose_name='产品型号(秘鲁)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='peru_spec',
            field=models.CharField(default='', max_length=200, verbose_name='产品规格(秘鲁)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='spanish_name',
            field=models.CharField(default='', max_length=200, verbose_name='产品型号(西班牙语)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='spanish_spec',
            field=models.CharField(default='', max_length=200, verbose_name='产品规格(西班牙语)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='spec',
            field=models.CharField(max_length=200, verbose_name='产品规格'),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='type_name',
            field=models.CharField(max_length=50, verbose_name='产品类名'),
        ),
    ]
