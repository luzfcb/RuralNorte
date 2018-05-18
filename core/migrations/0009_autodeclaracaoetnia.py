# Generated by Django 2.0.4 on 2018-04-24 23:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20180424_2017'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoDeclaracaoEtnia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_declaracao_etnia', models.IntegerField(choices=[(1, 'Negros'), (2, 'Pardos'), (3, 'Brancos'), (4, 'Índios'), (5, 'Orientais'), (6, 'Outros')], verbose_name='Etnia')),
                ('outros', models.CharField(blank=True, max_length=30, null=True, verbose_name='Outros')),
                ('quantidade', models.IntegerField(verbose_name='Quantos?')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('lote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='autoDeclaracoes', to='core.Lote', verbose_name='Lote')),
            ],
            options={
                'verbose_name': 'Quantos moradores se declaram?',
                'verbose_name_plural': 'Quantos moradores se declaram?',
            },
        ),
    ]
