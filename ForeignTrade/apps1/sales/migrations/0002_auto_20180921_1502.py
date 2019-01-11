# Generated by Django 2.1.1 on 2018-09-21 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sales', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='salescontract',
            name='salesman',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='业务员'),
        ),
        migrations.AddField(
            model_name='collectionplan',
            name='sales',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.SalesContract', verbose_name='销售合同'),
        ),
    ]
