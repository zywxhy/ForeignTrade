# Generated by Django 2.1.1 on 2019-01-10 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('branch_warehousing', '0001_initial'),
        ('domestic_invoice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='branchwarehousing',
            name='domestic_invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='domestic_invoice.DomesticInvoice', verbose_name='国内发货单'),
        ),
    ]
