# Generated by Django 3.0.5 on 2020-05-27 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20200527_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='final_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name=' '),
        ),
    ]