# Generated by Django 3.0.5 on 2020-05-30 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_auto_20200530_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(verbose_name=''),
        ),
    ]
