# Generated by Django 2.0.5 on 2018-12-13 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('invoice', '0001_initial'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='sales',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sales.SalesContract', verbose_name='销售合同'),
        ),
    ]
