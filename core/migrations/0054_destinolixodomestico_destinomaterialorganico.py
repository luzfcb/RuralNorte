# Generated by Django 2.0.4 on 2018-04-27 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0053_auto_20180427_1652'),
    ]

    operations = [
        migrations.CreateModel(
            name='DestinoLixoDomestico',
            fields=[
                ('lote', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='destinosLixoDomestico', serialize=False, to='core.Lote', verbose_name='Lote')),
                ('destino', models.IntegerField(choices=[(10, 'Espalhado no lote'), (20, 'Queima'), (30, 'Enterra'), (40, "Joga nos cursos d'água"), (50, 'Recicla/reaproveita lixo inorgânico'), (60, 'Deposita a céu aberto no lote')], verbose_name='Destino')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
            ],
            options={
                'verbose_name': 'Qual é o destino do lixo doméstico não orgânico?',
                'verbose_name_plural': 'Qual é o destino do lixo doméstico não orgânico?',
            },
        ),
        migrations.CreateModel(
            name='DestinoMaterialOrganico',
            fields=[
                ('lote', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='destinosMaterialOrganico', serialize=False, to='core.Lote', verbose_name='Lote')),
                ('destino', models.IntegerField(choices=[(10, 'Uso para alimentação de animais'), (20, 'Faz compostagem'), (30, 'Enterra junto com inorgânico'), (40, 'Deposita a céu aberto no lote')], verbose_name='Destino')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
            ],
            options={
                'verbose_name': 'Qual o destino do material inorgânico?',
                'verbose_name_plural': 'Qual o destino do material inorgânico?',
            },
        ),
    ]