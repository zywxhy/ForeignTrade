# Generated by Django 2.0.5 on 2019-01-04 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branch_warehousing', '0002_auto_20181226_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='branchwarehousingproduct',
            name='total_cost_price',
            field=models.FloatField(default=0, help_text='总成本', verbose_name='总成本'),
        ),
        migrations.AlterField(
            model_name='branchwarehousingproduct',
            name='warehousing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehousing_product', to='branch_warehousing.BranchWarehousing', verbose_name='海外入库单'),
        ),
    ]
