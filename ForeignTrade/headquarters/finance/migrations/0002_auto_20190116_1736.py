# Generated by Django 2.1.1 on 2019-01-16 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sales', '0001_initial'),
        ('purchase', '0001_initial'),
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='actualreceipts',
            name='sales',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.SalesContract', verbose_name='销售合同'),
        ),
        migrations.AddField(
            model_name='actualpayment',
            name='purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.PurchaseContract', verbose_name='采购合同'),
        ),
    ]