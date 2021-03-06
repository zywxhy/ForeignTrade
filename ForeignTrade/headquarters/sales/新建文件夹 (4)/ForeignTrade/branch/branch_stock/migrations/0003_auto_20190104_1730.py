# Generated by Django 2.0.5 on 2019-01-04 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branch_stock', '0002_branchstockrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branchstockproducts',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='branch_stock_product', to='branch_stock.BranchStock', verbose_name='仓库'),
        ),
    ]
