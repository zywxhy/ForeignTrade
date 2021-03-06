# Generated by Django 2.0.5 on 2019-01-09 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overseas_invoice', '0004_overseasinvoiceproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='overseasinvoiceproduct',
            name='real_count',
            field=models.IntegerField(default=0, help_text='实际出库数量', verbose_name='实际出库数量'),
        ),
        migrations.AlterField(
            model_name='overseasinvoiceproduct',
            name='count',
            field=models.IntegerField(default=0, help_text='预计出库数量', verbose_name='预计出库数量'),
        ),
    ]
