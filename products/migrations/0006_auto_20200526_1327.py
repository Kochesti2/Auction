# Generated by Django 3.0.5 on 2020-05-26 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20200526_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='min_increment',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]