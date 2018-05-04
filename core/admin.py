from django.contrib import admin
from . import models

class ProjetoAssentamentoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'municipio', 'contrato', 'data_criacao')
    search_fields = ['codigo', 'nome', 'municipio']
    list_filter = ['contrato', 'municipio', 'criado_em', 'atualizado_em']

class DocumentoLoteInlineAdmin(admin.StackedInline):
    model = models.DocumentoLote
    extra = 1

class BeneficioSocialInlineAdmin(admin.StackedInline):
    model = models.BeneficioSocial
    extra = 1

class EstruturaOrganizativaInlineAdmin(admin.StackedInline):
    model = models.EstruturaOrganizativa
    extra = 1

class AutoDeclaracaoEtniaInlineAdmin(admin.StackedInline):
    model = models.AutoDeclaracaoEtnia
    extra = 1

class FonteAguaInlineAdmin(admin.StackedInline):
    model = models.FonteAgua
    extra = 1

class TratamentoAguaInlineAdmin(admin.StackedInline):
    model = models.TratamentoAgua
    extra = 1

class ConstrucaoLoteInlineAdmin(admin.StackedInline):
    model = models.ConstrucaoLote
    extra = 1

class BemProdutivoInlineAdmin(admin.StackedInline):
    model = models.BemProdutivo
    extra = 1

class AplicacaoCreditoInlineAdmin(admin.StackedInline):
    model = models.AplicacaoCredito
    extra = 1

class CreditoBancarioInlineAdmin(admin.StackedInline):
    model = models.CreditoBancario
    extra = 1

class CulturaInlineAdmin(admin.StackedInline):
    model = models.Cultura
    exclude = ['classificacao']
    extra = 1

class OlericulturaInlineAdmin(admin.StackedInline):
    model = models.Olericultura
    exclude = ['classificacao']
    extra = 1

class FruticulturaInlineAdmin(admin.StackedInline):
    model = models.Fruticultura
    exclude = ['classificacao']
    extra = 1

class AtividadeExtrativistaInlineAdmin(admin.StackedInline):
    model = models.AtividadeExtrativista
    extra = 1

class ProducaoFlorestalInlineAdmin(admin.StackedInline):
    model = models.ProducaoFlorestal
    extra = 1

class BovinoculturaInlineAdmin(admin.StackedInline):
    model = models.Bovinocultura
    exclude = ['classificacao']
    extra = 1

class OutraCriacaoInlineAdmin(admin.StackedInline):
    model = models.OutraCriacao
    exclude = ['classificacao', 'tipo_criacao']
    extra = 1

class NivelTecnologicoProducaoAnimalInlineAdmin(admin.StackedInline):
    model = models.NivelTecnologicoProducaoAnimal

class ProblemaAmbientalInlineAdmin(admin.StackedInline):
    model = models.ProblemaAmbiental
    extra = 1

class PraticaConservacionistaInlineAdmin(admin.StackedInline):
    model = models.PraticaConservacionista
    extra = 1

class DestinoLixoDomesticoInlineAdmin(admin.StackedInline):
    model = models.DestinoLixoDomestico

class DestinoMaterialOrganicoInlineAdmin(admin.StackedInline):
    model = models.DestinoMaterialOrganico

class LicenciamentoAmbientalInlineAdmin(admin.StackedInline):
    model = models.LicenciamentoAmbiental
    extra = 1

class AtendimentoSaudeInlineAdmin(admin.StackedInline):
    model = models.AtendimentoSaude

class ProgramaSaudeInlineAdmin(admin.StackedInline):
    model = models.ProgramaSaude
    extra = 1

class AtividadeFisicaInlineAdmin(admin.StackedInline):
    model = models.AtividadeFisica
    extra = 1

class EspacoDisponivelInlineAdmin(admin.StackedInline):
    model = models.EspacoDisponivel
    extra = 1

class EstabelecimentoEnsinoInlineAdmin(admin.StackedInline):
    model = models.EstabelecimentoEnsino
    extra = 1

class BovinoculturaLeiteiraInlineAdmin(admin.StackedInline):
    model = models.BovinoculturaLeiteira
    exclude = ['tipo_criacao']
    extra = 1

class BovinoculturaCorteInlineAdmin(admin.StackedInline):
    model = models.BovinoculturaCorte
    exclude = ['tipo_criacao']
    extra = 1

class OrigemAnimalInlineAdmin(admin.StackedInline):
    model = models.OrigemAnimal
    exclude = ['classificacao']
    extra = 1

class ProcessadoBeneficiadoInlineAdmin(admin.StackedInline):
    model = models.ProcessadoBeneficiado
    exclude = ['classificacao']
    extra = 1

class LoteAdmin(admin.ModelAdmin):
    list_display = ('codigo_sipra', 'area', 'numero', 'projeto_assentamento')
    search_fields = ['codigo_sipra', 'numero']
    list_filter = [
        'projeto_assentamento', 'entrevistador', 'outra_familia_no_lote', 'cad_unico', 'ocupante_irregular',
        'recebe_beneficio_social', 'moradia_assentamento', 'tipo_parede_externa', 'tipo_instalacao_eletrica',
        'tipo_instalacao_sanitaria', 'localizacao_fonte_agua', 'abastecimento_agua_suficiente',
        'quantas_familias_utilizam_mesma_fonte_agua', 'agua_para_animais_plantio', 'regularidade_abastecimento_agua',
        'tipo_estrada_acesso', 'situacao_estrada_acesso', 'situacao_cercado_lote', 'area_preservacao_permanente',
        'area_preservacao_permanente_cercada', 'necessita_licenciamento_ambiental',
        'necessita_autoriacao_exploracao_florestal_queima_controlada', 'documentos', 'beneficios', 'autoDeclaracoes',
        'estruturasOrganizativas', 'fontesAgua', 'tratamentosAgua', 'construcoesLote', 'bensProdutivos',
        'aplicacoesCredito', 'creditosBancarios'
    ]
    inlines = [
        DocumentoLoteInlineAdmin, BeneficioSocialInlineAdmin, AutoDeclaracaoEtniaInlineAdmin, EstruturaOrganizativaInlineAdmin,
        FonteAguaInlineAdmin, TratamentoAguaInlineAdmin, ConstrucaoLoteInlineAdmin,  BemProdutivoInlineAdmin,
        AplicacaoCreditoInlineAdmin, CreditoBancarioInlineAdmin, CulturaInlineAdmin, OlericulturaInlineAdmin,
        FruticulturaInlineAdmin, AtividadeExtrativistaInlineAdmin, ProducaoFlorestalInlineAdmin,
        BovinoculturaInlineAdmin, OutraCriacaoInlineAdmin, BovinoculturaLeiteiraInlineAdmin, BovinoculturaCorteInlineAdmin,
        OrigemAnimalInlineAdmin, NivelTecnologicoProducaoAnimalInlineAdmin, ProcessadoBeneficiadoInlineAdmin,
        ProblemaAmbientalInlineAdmin, PraticaConservacionistaInlineAdmin, DestinoLixoDomesticoInlineAdmin,
        DestinoMaterialOrganicoInlineAdmin, LicenciamentoAmbientalInlineAdmin, AtendimentoSaudeInlineAdmin,
        ProgramaSaudeInlineAdmin, AtividadeFisicaInlineAdmin, EspacoDisponivelInlineAdmin, EstabelecimentoEnsinoInlineAdmin
    ]
    exclude = ['necessita_licenciamento_ambiental']

admin.site.register(models.ProjetoAssentamento, ProjetoAssentamentoAdmin)
admin.site.register(models.Lote, LoteAdmin)