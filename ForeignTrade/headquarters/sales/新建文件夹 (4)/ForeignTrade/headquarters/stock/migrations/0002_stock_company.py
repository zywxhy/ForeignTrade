# Generated by Django 2.0.5 on 2018-12-13 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.Company', verbose_name='所在公司'),
        ),
    ]
