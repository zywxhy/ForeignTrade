# Generated by Django 2.0.5 on 2018-12-25 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_contacter'),
        ('product', '0001_initial'),
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
                'verbose_name': '仓库',
                'verbose_name_plural': '仓库',
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
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='branch_stock.BranchStock', verbose_name='仓库')),
            ],
        ),
    ]
