# Generated by Django 2.1.1 on 2018-09-21 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_num', models.CharField(default='', max_length=30, unique=True, verbose_name='采购单号')),
                ('sales_num', models.CharField(default='', max_length=30, verbose_name='合同编号')),
                ('date', models.CharField(default='', max_length=30, unique=True, verbose_name='采购时间')),
                ('account_period', models.IntegerField(default=0, verbose_name='账期')),
                ('reviewer', models.CharField(default='', max_length=30, unique=True, verbose_name='审批人')),
                ('currency', models.CharField(default='', max_length=30, unique=True, verbose_name='币种')),
                ('exrate', models.CharField(default='', max_length=30, unique=True, verbose_name='汇率')),
                ('bill_name', models.CharField(default='', max_length=30, unique=True, verbose_name='开票名称')),
                ('bill_unit', models.CharField(default='', max_length=30, unique=True, verbose_name='开票单位')),
                ('bill_quantity', models.CharField(default='', max_length=30, unique=True, verbose_name='开票数量')),
                ('bill_amount', models.CharField(default='', max_length=30, unique=True, verbose_name='开票金额')),
                ('not_bill_amount', models.CharField(default='', max_length=30, unique=True, verbose_name='未开票金额')),
                ('total_amount', models.CharField(default='', max_length=30, unique=True, verbose_name='总金额')),
                ('serial_number', models.IntegerField(default=1)),
                ('status', models.IntegerField(choices=[(0, '未审核'), (1, '已审核'), (2, '已入库(全部)'), (3, '已完成(付款完毕)'), (4, '已退货(全部)')], default=0, verbose_name='订单状态')),
            ],
            options={
                'verbose_name': '采购订单',
                'verbose_name_plural': '采购订单',
            },
        ),
        migrations.CreateModel(
            name='PurchaseProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.CharField(default='', max_length=200, verbose_name='备注')),
                ('count', models.IntegerField(verbose_name='数量')),
                ('outbound_count', models.IntegerField(default=0, verbose_name='入库数量')),
                ('return_count', models.IntegerField(default=0, verbose_name='退货数量')),
                ('unit_price', models.FloatField(verbose_name='单价')),
                ('status', models.IntegerField(default=0, verbose_name='预留字段')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.Product', verbose_name='产品')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.PurchaseContract', verbose_name='采购合同')),
            ],
            options={
                'verbose_name': '订单内产品',
                'verbose_name_plural': '订单内产品',
            },
        ),
    ]
