# Generated by Django 2.0.5 on 2018-07-26 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membro',
            name='escolaridade',
            field=models.IntegerField(choices=[(10, '(a) Não alfabetizado'), (20, '(b) 1º ao 4º ano'), (30, '(c) 5º ao 9º ano'), (40, '(d) Fundamental completo'), (50, '(e) EJA - Educação de Jovens e Adultos'), (60, '(f) Médio incompleto'), (70, '(g) Médio completo'), (80, '(h) Superior incompleto'), (90, '(i) Superior completo'), (100, '(j) Pós Graduação incompleto'), (110, '(k) Pós Graduação completo')], verbose_name='Escolaridade'),
        ),
        migrations.AlterField(
            model_name='membro',
            name='opcao_ensino_utilizada_distancia_ate_escola',
            field=models.IntegerField(blank=True, null=True, verbose_name='Distância até a escola (Km)'),
        ),
        migrations.AlterField(
            model_name='membro',
            name='opcao_ensino_utilizada_oferta_de_transporte',
            field=models.IntegerField(blank=True, choices=[(1, 'Sim'), (0, 'Não')], null=True, verbose_name='Há oferta de transporte para a escola?'),
        ),
    ]
