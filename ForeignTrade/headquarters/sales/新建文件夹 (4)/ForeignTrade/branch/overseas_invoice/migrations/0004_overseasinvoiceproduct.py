# Generated by Django 2.0.5 on 2019-01-09 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('overseas_invoice', '0003_auto_20190109_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='OverseasInvoiceProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0, help_text='出库数量', verbose_name='出库数量')),
                ('overseas_invoice', models.ForeignKey(help_text='出库单', on_delete=django.db.models.deletion.CASCADE, related_name='overseas_invoice_product', to='overseas_invoice.OverseasInvoice', verbose_name='出库单')),
                ('product', models.ForeignKey(help_text='出库产品', on_delete=django.db.models.deletion.PROTECT, to='product.Product', verbose_name='出库产品')),
            ],
        ),
    ]
