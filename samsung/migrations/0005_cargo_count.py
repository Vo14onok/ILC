# Generated by Django 2.0.5 on 2018-07-18 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samsung', '0004_auto_20180717_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='cargo',
            name='count',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=4, verbose_name='Стоимость'),
            preserve_default=False,
        ),
    ]