# Generated by Django 2.0.5 on 2019-01-12 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch_sales', '0004_remove_branchsalescontract_price_clause'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branchsalesproduct',
            options={'verbose_name': '分公司销售合同产品', 'verbose_name_plural': '分公司销售合同产品'},
        ),
        migrations.AddField(
            model_name='branchsalescontract',
            name='shipping_fee',
            field=models.FloatField(default=0, verbose_name='运费'),
        ),
    ]
