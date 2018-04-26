from django.contrib import admin
from .models import *

class ProjetoAssentamentoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'municipio', 'contrato', 'data_criacao')
    search_fields = ['codigo', 'nome', 'municipio']
    list_filter = ['contrato', 'municipio', 'criado_em', 'atualizado_em']

class DocumentoLoteInlineAdmin(admin.StackedInline):
    model = DocumentoLote
    extra = 1

class BeneficioSocialInlineAdmin(admin.StackedInline):
    model = BeneficioSocial
    extra = 1

class EstruturaOrganizativaInlineAdmin(admin.StackedInline):
    model = EstruturaOrganizativa
    extra = 1

class AutoDeclaracaoEtniaInlineAdmin(admin.StackedInline):
    model = AutoDeclaracaoEtnia
    extra = 1

class FonteAguaInlineAdmin(admin.StackedInline):
    model = FonteAgua
    extra = 1

class TratamentoAguaInlineAdmin(admin.StackedInline):
    model = TratamentoAgua
    extra = 1

class ConstrucaoLoteInlineAdmin(admin.StackedInline):
    model = ConstrucaoLote
    extra = 1

class BemProdutivoInlineAdmin(admin.StackedInline):
    model = BemProdutivo
    extra = 1

class AplicacaoCreditoInlineAdmin(admin.StackedInline):
    model = AplicacaoCredito
    extra = 1

class CreditoBancarioInlineAdmin(admin.StackedInline):
    model = CreditoBancario
    extra = 1

class CulturaInlineAdmin(admin.StackedInline):
    model = Cultura
    exclude = ['classificacao']
    extra = 1

class OlericulturaInlineAdmin(admin.StackedInline):
    model = Olericultura
    exclude = ['classificacao']
    extra = 1

class FruticulturaInlineAdmin(admin.StackedInline):
    model = Fruticultura
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
        'tipo_estrada_acesso', 'situacao_estrada_acesso', 'situacao_cercado_lote', 'documentos', 'beneficios',
        'autoDeclaracoes', 'estruturasOrganizativas', 'fontesAgua', 'tratamentosAgua', 'construcoesLote',
        'bensProdutivos', 'aplicacoesCredito', 'creditosBancarios'
    ]
    inlines = [
        DocumentoLoteInlineAdmin, BeneficioSocialInlineAdmin, AutoDeclaracaoEtniaInlineAdmin, EstruturaOrganizativaInlineAdmin,
        FonteAguaInlineAdmin, TratamentoAguaInlineAdmin, ConstrucaoLoteInlineAdmin,  BemProdutivoInlineAdmin,
        AplicacaoCreditoInlineAdmin, CreditoBancarioInlineAdmin, CulturaInlineAdmin, OlericulturaInlineAdmin,
        FruticulturaInlineAdmin
    ]

admin.site.register(ProjetoAssentamento, ProjetoAssentamentoAdmin)
admin.site.register(Lote, LoteAdmin)