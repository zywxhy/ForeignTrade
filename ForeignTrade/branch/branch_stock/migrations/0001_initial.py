# Generated by Django 2.1.1 on 2019-01-17 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BranchStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, unique=True, verbose_name='仓库名')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.Company', verbose_name='所属公司')),
            ],
            options={
                'verbose_name': '海外仓库',
                'verbose_name_plural': '海外仓库',
            },
        ),
        migrations.CreateModel(
            name='BranchStockProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0, verbose_name='总数量')),
                ('sr_count', models.IntegerField(default=0, verbose_name='在途数量')),
                ('por_count', models.IntegerField(default=0, verbose_name='需求数量')),
                ('unit_cost', models.FloatField(default=0, verbose_name='平均成本')),
                ('bad_count', models.IntegerField(default=0, verbose_name='不良品数量')),
                ('recent_date', models.DateField(default='2000-01-01', verbose_name='最近入库时间')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.Product', verbose_name='库存产品')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='branch_stock_product', to='branch_stock.BranchStock', verbose_name='仓库')),
            ],
        ),
        migrations.CreateModel(
            name='BranchStockRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maker', models.CharField(max_length=20, verbose_name='申请人')),
                ('reviewer', models.CharField(max_length=20, verbose_name='审批人')),
                ('odd_num', models.CharField(max_length=20, verbose_name='单号')),
                ('unit_price', models.FloatField(default=0, verbose_name='售价')),
                ('cost_unit_price', models.FloatField(default=0, verbose_name='成本')),
                ('count', models.IntegerField(default=0, verbose_name='数量')),
                ('type', models.IntegerField(choices=[(0, '出库'), (1, '入库')], default=0, verbose_name='类型')),
                ('reason', models.CharField(default='normal', max_length=300, verbose_name='原因')),
                ('date', models.DateField(default='2000-01-01', verbose_name='日期')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.Product', verbose_name='产品')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='branch_stock.BranchStock', verbose_name='仓库')),
            ],
        ),
    ]