# Generated by Django 2.1.1 on 2019-01-17 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('branch_stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BranchWarehousing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warehousing_num', models.CharField(default='', max_length=20, unique=True, verbose_name='入库单号')),
                ('warehousing_date', models.DateField(default='2000-01-01', verbose_name='入库时间')),
                ('share_cost', models.FloatField(default=0, verbose_name='均摊总成本')),
                ('status', models.IntegerField(default=0, verbose_name='入库状态')),
                ('remark', models.CharField(default='', max_length=500, verbose_name='备注')),
                ('branch_stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branch_stock.BranchStock', verbose_name='仓库')),
            ],
        ),
        migrations.CreateModel(
            name='BranchWarehousingProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_cost_price', models.FloatField(default=0, help_text='总成本', verbose_name='总成本')),
                ('count', models.IntegerField(default=0, verbose_name='入库数量')),
                ('remark', models.CharField(default='', max_length=200, null=True, verbose_name='备注')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product', verbose_name='入库产品')),
                ('warehousing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehousing_product', to='branch_warehousing.BranchWarehousing', verbose_name='海外入库单')),
            ],
        ),
    ]
