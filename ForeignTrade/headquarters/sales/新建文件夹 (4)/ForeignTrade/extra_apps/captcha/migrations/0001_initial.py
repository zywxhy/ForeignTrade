# Generated by Django 2.0.5 on 2018-09-17 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CaptchaStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('challenge', models.CharField(max_length=32)),
                ('response', models.CharField(max_length=32)),
                ('hashkey', models.CharField(max_length=40, unique=True)),
                ('expiration', models.DateTimeField()),
            ],
        ),
    ]
