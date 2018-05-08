# Generated by Django 2.0.4 on 2018-04-27 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_fruticultura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='regularidade_abastecimento_agua',
            field=models.IntegerField(choices=[(1, 'Sempre tem água'), (2, 'Falta água às vezes'), (3, 'Falta água com frequência'), (4, 'Nunca tem água')], verbose_name='Regularidade de abastecimento de água'),
        ),
    ]