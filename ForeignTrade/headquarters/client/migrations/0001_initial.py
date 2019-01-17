# Generated by Django 2.1.1 on 2019-01-16 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(default='', max_length=50, unique=True, verbose_name='客户代码')),
                ('name', models.CharField(default='', max_length=100, verbose_name='客户名')),
                ('company_name', models.CharField(default='', max_length=100, verbose_name='客户公司名')),
                ('credit', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='5', max_length=10, verbose_name='客户信用')),
                ('level', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='1', max_length=10, verbose_name='客户级别')),
                ('info', models.CharField(default='', max_length=100, verbose_name='客户信息')),
                ('is_branch', models.BooleanField(default=False, verbose_name='是否分公司')),
                ('recent_date', models.DateField(verbose_name='最近时间')),
            ],
            options={
                'verbose_name': '客户信息',
                'verbose_name_plural': '客户信息',
            },
        ),
        migrations.CreateModel(
            name='ClientContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(default='', max_length=50, unique=True, verbose_name='邮箱')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.Client', verbose_name='客户')),
            ],
        ),
        migrations.CreateModel(
            name='ContinentsState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('continent_cname', models.CharField(default='', max_length=50, verbose_name='所在大洲')),
                ('continent_name', models.CharField(default='', max_length=50, verbose_name='所在大洲(英文)')),
                ('country_cname', models.CharField(default='', max_length=50, verbose_name='地区')),
                ('country_name', models.CharField(default='', max_length=50, verbose_name='地区(英文)')),
                ('is_parent', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': '大洲国家表',
                'verbose_name_plural': '大洲国家表',
            },
        ),
        migrations.AddField(
            model_name='client',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='area', to='client.ContinentsState', verbose_name='地区'),
        ),
    ]