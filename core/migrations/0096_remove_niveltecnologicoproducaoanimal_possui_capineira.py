# Generated by Django 2.0.4 on 2018-05-14 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0095_lote_possui_capineira'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='niveltecnologicoproducaoanimal',
            name='possui_capineira',
        ),
    ]