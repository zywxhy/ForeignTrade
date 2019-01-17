# Generated by Django 2.1.1 on 2019-01-16 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt', models.FloatField(default=0, verbose_name='收款金额')),
                ('receipt_type', models.CharField(max_length=30, verbose_name='收款方式')),
                ('receipt_date', models.DateField(verbose_name='预计时间')),
                ('remark', models.CharField(default='', max_length=100, verbose_name='备注')),
            ],
            options={
                'verbose_name': '收款计划',
                'verbose_name_plural': '收款计划',
            },
        ),
        migrations.CreateModel(
            name='SalesContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_num', models.CharField(default='', max_length=20, unique=True, verbose_name='合同编号')),
                ('buyer', models.CharField(default='', max_length=20, verbose_name='采购员')),
                ('maker', models.CharField(default='', max_length=20, verbose_name='制单人')),
                ('date', models.DateField(verbose_name='签约日期')),
                ('shipment_port', models.CharField(default='', max_length=30, verbose_name='装运口岸')),
                ('destination_port', models.CharField(default='', max_length=30, verbose_name='目的口岸')),
                ('currency', models.CharField(max_length=20, verbose_name='币种')),
                ('price_clause', models.CharField(max_length=10, verbose_name='价格条款')),
                ('export_company', models.CharField(max_length=20, verbose_name='出口公司')),
                ('mode_of_transport', models.CharField(choices=[('空运', '空运'), ('海运', '海运'), ('快递', '快递')], max_length=20, verbose_name='运输方式')),
                ('exrate', models.FloatField(default=1, verbose_name='汇率')),
                ('status', models.IntegerField(choices=[(0, '未审核'), (1, '已审核'), (2, '已采购'), (3, '已出库(全部)'), (4, '已完成(收款完毕)'), (5, '已退货(全部)')], default=0, verbose_name='合同状态')),
                ('shipping_fee', models.FloatField(default=0, verbose_name='运费')),
                ('insurance', models.FloatField(default=0, verbose_name='保险费')),
                ('other_fee', models.FloatField(default=0, verbose_name='其他费用')),
                ('total_amount', models.FloatField(default=0, verbose_name='总金额')),
                ('invoice_index', models.IntegerField(default=1, verbose_name='出库单序号')),
                ('refund_index', models.IntegerField(default=1, verbose_name='退货单序号')),
                ('remark', models.CharField(default='', max_length=300, verbose_name='备注')),
            ],
            options={
                'verbose_name': '销售合同',
                'verbose_name_plural': '销售合同',
            },
        ),
        migrations.CreateModel(
            name='SalesProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.CharField(default='', max_length=200, verbose_name='备注')),
                ('volume', models.FloatField(default=0, verbose_name='体积')),
                ('sales_count', models.IntegerField(verbose_name='销售数量')),
                ('outbound_count', models.IntegerField(default=0, verbose_name='出库数量')),
                ('return_count', models.IntegerField(default=0, verbose_name='退货数量')),
                ('purchase_count', models.IntegerField(default=0, verbose_name='采购数量')),
                ('unit_price', models.FloatField(verbose_name='单价')),
                ('amount', models.FloatField(verbose_name='金额')),
                ('discount', models.FloatField(default=0, verbose_name='折扣')),
                ('receivable_amount', models.FloatField(default=0, verbose_name='应收金额')),
                ('status', models.IntegerField(default=0, verbose_name='预留字段')),
            ],
            options={
                'verbose_name': '合同内产品',
                'verbose_name_plural': '合同内产品',
            },
        ),
        migrations.CreateModel(
            name='SalesStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0, verbose_name='数量')),
                ('year', models.IntegerField(default=2018, verbose_name='年')),
                ('month', models.IntegerField(default=1, verbose_name='月')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='client.Client', verbose_name='客户')),
            ],
        ),
    ]
