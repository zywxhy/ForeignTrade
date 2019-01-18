# Generated by Django 2.1.1 on 2019-01-17 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductTaxRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_rate', models.FloatField(default=0, verbose_name='税率')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.Company', verbose_name='分公司')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.Product', verbose_name='产品')),
            ],
        ),
    ]