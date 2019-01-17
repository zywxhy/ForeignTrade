# Generated by Django 2.0.5 on 2018-12-13 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=150, unique=True, verbose_name='客户名')),
                ('account_period', models.IntegerField(default=0, verbose_name='账期')),
                ('area', models.CharField(default='', max_length=50, verbose_name='地区')),
                ('address', models.CharField(default='', max_length=200, verbose_name='地址')),
                ('eco_nature', models.CharField(default='', max_length=20, verbose_name='经济性质')),
                ('bank_account', models.CharField(default='', max_length=50, verbose_name='银行账户')),
                ('bank', models.CharField(default='', max_length=50, verbose_name='开户银行')),
                ('duty_para', models.CharField(default='', max_length=50, verbose_name='税号')),
                ('postalcode', models.CharField(default='', max_length=50, verbose_name='邮政编码')),
                ('fax', models.CharField(default='', max_length=50, verbose_name='传真')),
                ('telephone', models.CharField(default='', max_length=50, verbose_name='电话')),
                ('inputting_date', models.DateField(verbose_name='建档时间')),
                ('is_head_office', models.BooleanField(default=False, verbose_name='是否总公司')),
            ],
            options={
                'verbose_name': '供应商',
                'verbose_name_plural': '供应商',
            },
        ),
        migrations.CreateModel(
            name='SupplierContacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, verbose_name='联系人名字')),
                ('phone', models.CharField(default='', max_length=50, verbose_name='联系电话')),
                ('telephone', models.CharField(default='', max_length=50, verbose_name='手机号码')),
                ('fax', models.CharField(default='', max_length=50, verbose_name='传真')),
                ('email', models.CharField(default='', max_length=50, verbose_name='邮箱')),
                ('position', models.CharField(default='', max_length=50, verbose_name='职位')),
                ('master_contact', models.BooleanField(default=False, verbose_name='主联系人')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.Supplier', verbose_name='供应商')),
            ],
            options={
                'verbose_name': '供应商相关联系人',
                'verbose_name_plural': '供应商相关联系人',
            },
        ),
        migrations.CreateModel(
            name='SupplierProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.Product', verbose_name='产品')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.Supplier', verbose_name='供应商')),
            ],
            options={
                'verbose_name': '供应商产品',
                'verbose_name_plural': '供应商产品',
            },
        ),
    ]
