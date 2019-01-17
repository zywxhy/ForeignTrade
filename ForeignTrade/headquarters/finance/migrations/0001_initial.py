# Generated by Django 2.1.1 on 2019-01-16 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActualPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_amount', models.FloatField(default=0, verbose_name='付款金额')),
                ('payment_type', models.CharField(max_length=30, verbose_name='付款方式')),
                ('payment_date', models.DateField(verbose_name='付款时间')),
                ('remark', models.CharField(default='', max_length=100, verbose_name='备注')),
            ],
            options={
                'verbose_name': '实际付款',
                'verbose_name_plural': '实际付款',
            },
        ),
        migrations.CreateModel(
            name='ActualReceipts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt', models.FloatField(default=0, verbose_name='收款金额')),
                ('receipt_type', models.CharField(max_length=30, verbose_name='收款方式')),
                ('receipt_date', models.DateField(verbose_name='收款时间')),
                ('remark', models.CharField(default='', max_length=100, verbose_name='备注')),
            ],
            options={
                'verbose_name': '实际收款',
                'verbose_name_plural': '实际收款',
            },
        ),
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(max_length=50, verbose_name='币种')),
                ('type', models.CharField(max_length=20, verbose_name='兑换货币')),
                ('date', models.DateField(verbose_name='修改时间')),
                ('exchange_rate', models.FloatField(default=1, verbose_name='汇率')),
            ],
            options={
                'verbose_name': '汇率',
                'verbose_name_plural': '汇率',
            },
        ),
    ]
