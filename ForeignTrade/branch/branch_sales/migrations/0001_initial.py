# Generated by Django 2.1.1 on 2019-01-17 16:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('branch_client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BranchSalesCollections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='BranchSalesContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_num', models.CharField(default='', max_length=20, unique=True, verbose_name='合同编号')),
                ('maker', models.CharField(default='', max_length=20, verbose_name='制单人')),
                ('sales_date', models.DateField(verbose_name='签约日期')),
                ('currency', models.CharField(max_length=20, verbose_name='币种')),
                ('shipping_fee', models.FloatField(default=0, verbose_name='运费')),
                ('status', models.IntegerField(choices=[(0, '报价阶段'), (1, '销售订单'), (2, '审核失败'), (3, '已出库(全部)'), (4, '已完成(收款完毕)'), (5, '欠款'), (6, '退货')], default=0, verbose_name='合同状态')),
                ('total_amount', models.FloatField(default=0, verbose_name='总金额')),
                ('remark', models.CharField(default='', max_length=300, verbose_name='备注')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='branch_client.BranchClient', verbose_name='海外分公司客户')),
                ('salesman', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='业务员')),
            ],
            options={
                'verbose_name': '分公司销售合同',
                'verbose_name_plural': '分公司销售合同',
            },
        ),
        migrations.CreateModel(
            name='BranchSalesProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.CharField(default='', max_length=200, verbose_name='备注')),
                ('sales_count', models.IntegerField(verbose_name='销售数量')),
                ('outbound_count', models.IntegerField(default=0, verbose_name='出库数量')),
                ('return_count', models.IntegerField(default=0, verbose_name='退货数量')),
                ('unit_price', models.FloatField(verbose_name='单价')),
                ('amount', models.FloatField(verbose_name='金额')),
                ('discount', models.FloatField(default=0, verbose_name='折扣')),
                ('receivable_amount', models.FloatField(default=0, verbose_name='应收金额')),
                ('status', models.IntegerField(default=0, verbose_name='预留字段')),
                ('branch_sales', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_sales_product', to='branch_sales.BranchSalesContract', verbose_name='分公司销售合同')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.Product', verbose_name='产品')),
            ],
            options={
                'verbose_name': '分公司销售合同产品',
                'verbose_name_plural': '分公司销售合同产品',
            },
        ),
    ]