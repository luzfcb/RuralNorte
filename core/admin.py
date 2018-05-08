from django.contrib import admin
import nested_admin
from . import models
from django import forms


class FruticulturaFormAdmin(forms.ModelForm):
    tipo_producao = forms.ChoiceField(
        choices=(('', '---------'),) + models.Fruticultura.FRUTICULTURA + ((99, 'Outros'),))

    class Meta:
        model = models.Fruticultura
        fields = '__all__'


class ProjetoAssentamentoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'municipio', 'contrato', 'data_criacao')
    search_fields = ['codigo', 'nome', 'municipio']
    list_filter = ['contrato', 'municipio', 'cadastrado_em', 'modificado_em']


class OpcaoEnsinoUtilizadaInlineAdmin(nested_admin.NestedStackedInline):
    model = models.OpcaoEnsinoUtilizada
    exclude = ['desativado_por', 'desativado_em']
    delete = False


class UsoFrequenteInlineAdmin(nested_admin.NestedStackedInline):
    model = models.UsoFrequente
    exclude = ['desativado_por', 'desativado_em']
    extra = 1
    delete = False


class RendaTrabalhoForaLoteInlineAdmin(nested_admin.NestedStackedInline):
    model = models.RendaTrabalhoForaLote
    exclude = ['desativado_por', 'desativado_em']
    delete = False


class MembroInlineAdmin(nested_admin.NestedStackedInline):
    model = models.Membro
    exclude = ['desativado_por', 'desativado_em']
    extra = 1
    delete = False
    inlines = [RendaTrabalhoForaLoteInlineAdmin, UsoFrequenteInlineAdmin, OpcaoEnsinoUtilizadaInlineAdmin]


class FamiliaInlineAdmin(nested_admin.NestedStackedInline):
    model = models.Familia
    exclude = ['desativado_por', 'desativado_em']
    extra = 1
    delete = False
    inlines = [MembroInlineAdmin]


class ContatoInlineAdmin(admin.StackedInline):
    model = models.Contato
    exclude = ['desativado_por', 'desativado_em']
    extra = 1


class DocumentoLoteInlineAdmin(admin.StackedInline):
    model = models.DocumentoLote
    exclude = ['desativado_por', 'desativado_em']
    extra = 1


class BeneficioSocialInlineAdmin(admin.StackedInline):
    model = models.BeneficioSocial
    exclude = ['desativado_por', 'desativado_em']
    extra = 1


class EstruturaOrganizativaInlineAdmin(admin.StackedInline):
    model = models.EstruturaOrganizativa
    exclude = ['desativado_por', 'desativado_em']
    extra = 1


class AutoDeclaracaoEtniaInlineAdmin(admin.StackedInline):
    model = models.AutoDeclaracaoEtnia
    exclude = ['desativado_por', 'desativado_em']
    extra = 1


class FonteAguaInlineAdmin(admin.StackedInline):
    model = models.FonteAgua
    exclude = ['desativado_por', 'desativado_em']
    extra = 1


class TratamentoAguaInlineAdmin(admin.StackedInline):
    model = models.TratamentoAgua
    exclude = ['desativado_por', 'desativado_em']
    extra = 1


class ConstrucaoLoteInlineAdmin(admin.StackedInline):
    model = models.ConstrucaoLote
    exclude = ['desativado_por', 'desativado_em']
    extra = 1


class BemProdutivoInlineAdmin(admin.StackedInline):
    model = models.BemProdutivo
    exclude = ['desativado_por', 'desativado_em']
    extra = 1


class AplicacaoCreditoInlineAdmin(admin.StackedInline):
    model = models.AplicacaoCredito
    exclude = ['desativado_por', 'desativado_em']
    extra = 1


class CreditoBancarioInlineAdmin(admin.StackedInline):
    model = models.CreditoBancario
    exclude = ['desativado_por', 'desativado_em']
    extra = 1


class CulturaInlineAdmin(admin.StackedInline):
    model = models.Cultura
    exclude = ['classificacao', 'desativado_por', 'desativado_em']
    extra = 1


class OlericulturaInlineAdmin(admin.StackedInline):
    model = models.Olericultura
    exclude = ['classificacao', 'desativado_por', 'desativado_em']
    extra = 1


class FruticulturaInlineAdmin(admin.StackedInline):
    model = models.Fruticultura
    exclude = ['classificacao', 'desativado_por', 'desativado_em']
    extra = 1
    form = FruticulturaFormAdmin


class AtividadeExtrativistaInlineAdmin(admin.StackedInline):
    model = models.AtividadeExtrativista
    exclude = ['desativado_por', 'desativado_em']
    extra = 1


class ProducaoFlorestalInlineAdmin(admin.StackedInline):
    model = models.ProducaoFlorestal
    exclude = ['desativado_por', 'desativado_em']
    extra = 1


class BovinoculturaInlineAdmin(admin.StackedInline):
    model = models.Bovinocultura
    exclude = ['classificacao', 'desativado_por', 'desativado_em']
    extra = 1


class OutraCriacaoInlineAdmin(admin.StackedInline):
    model = models.OutraCriacao
    exclude = ['classificacao', 'tipo_criacao', 'desativado_por', 'desativado_em']
    extra = 1


class NivelTecnologicoProducaoAnimalInlineAdmin(admin.StackedInline):
    model = models.NivelTecnologicoProducaoAnimal
    exclude = ['desativado_por', 'desativado_em']


class ProblemaAmbientalInlineAdmin(admin.StackedInline):
    model = models.ProblemaAmbiental
    extra = 1


class PraticaConservacionistaInlineAdmin(admin.StackedInline):
    model = models.PraticaConservacionista
    exclude = ['desativado_por', 'desativado_em']
    extra = 1


class DestinoLixoDomesticoInlineAdmin(admin.StackedInline):
    model = models.DestinoLixoDomestico
    exclude = ['desativado_por', 'desativado_em']


class DestinoMaterialOrganicoInlineAdmin(admin.StackedInline):
    model = models.DestinoMaterialOrganico
    exclude = ['desativado_por', 'desativado_em']


class LicenciamentoAmbientalInlineAdmin(admin.StackedInline):
    model = models.LicenciamentoAmbiental
    exclude = ['desativado_por', 'desativado_em']
    extra = 1


class AtendimentoSaudeInlineAdmin(admin.StackedInline):
    model = models.AtendimentoSaude
    exclude = ['desativado_por', 'desativado_em']


class ProgramaSaudeInlineAdmin(admin.StackedInline):
    model = models.ProgramaSaude
    exclude = ['desativado_por', 'desativado_em']
    extra = 1


class AtividadeFisicaInlineAdmin(admin.StackedInline):
    model = models.AtividadeFisica
    exclude = ['desativado_por', 'desativado_em']
    extra = 1


class EspacoDisponivelInlineAdmin(admin.StackedInline):
    model = models.EspacoDisponivel
    exclude = ['desativado_por', 'desativado_em']
    extra = 1


class EstabelecimentoEnsinoInlineAdmin(admin.StackedInline):
    model = models.EstabelecimentoEnsino
    exclude = ['desativado_por', 'desativado_em']
    extra = 1


class BovinoculturaLeiteiraInlineAdmin(admin.StackedInline):
    model = models.BovinoculturaLeiteira
    exclude = ['tipo_criacao', 'desativado_por', 'desativado_em']
    extra = 1


class BovinoculturaCorteInlineAdmin(admin.StackedInline):
    model = models.BovinoculturaCorte
    exclude = ['tipo_criacao', 'desativado_por', 'desativado_em']
    extra = 1


class OrigemAnimalInlineAdmin(admin.StackedInline):
    model = models.OrigemAnimal
    exclude = ['classificacao', 'desativado_por', 'desativado_em']
    extra = 1


class ProcessadoBeneficiadoInlineAdmin(admin.StackedInline):
    model = models.ProcessadoBeneficiado
    exclude = ['classificacao', 'desativado_por', 'desativado_em']
    extra = 1


class NaoPossuiDocumentoInlineAdmin(admin.StackedInline):
    model = models.NaoPossuiDocumento
    exclude = ['desativado_por', 'desativado_em']


class LoteAdmin(nested_admin.NestedModelAdmin):
    list_display = ('codigo_sipra', 'area', 'numero', 'projeto_assentamento', 'outra_familia_no_lote', 'tipo_parede_externa')

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
        FamiliaInlineAdmin, ContatoInlineAdmin, DocumentoLoteInlineAdmin, BeneficioSocialInlineAdmin,
        AutoDeclaracaoEtniaInlineAdmin, EstruturaOrganizativaInlineAdmin, FonteAguaInlineAdmin,
        TratamentoAguaInlineAdmin,
        ConstrucaoLoteInlineAdmin, BemProdutivoInlineAdmin, AplicacaoCreditoInlineAdmin, CreditoBancarioInlineAdmin,
        CulturaInlineAdmin, OlericulturaInlineAdmin, FruticulturaInlineAdmin, AtividadeExtrativistaInlineAdmin,
        ProducaoFlorestalInlineAdmin, BovinoculturaInlineAdmin, OutraCriacaoInlineAdmin,
        BovinoculturaLeiteiraInlineAdmin,
        BovinoculturaCorteInlineAdmin, OrigemAnimalInlineAdmin, NivelTecnologicoProducaoAnimalInlineAdmin,
        ProcessadoBeneficiadoInlineAdmin, ProblemaAmbientalInlineAdmin, PraticaConservacionistaInlineAdmin,
        DestinoLixoDomesticoInlineAdmin, DestinoMaterialOrganicoInlineAdmin, LicenciamentoAmbientalInlineAdmin,
        AtendimentoSaudeInlineAdmin, ProgramaSaudeInlineAdmin, AtividadeFisicaInlineAdmin, EspacoDisponivelInlineAdmin,
        EstabelecimentoEnsinoInlineAdmin, NaoPossuiDocumentoInlineAdmin
    ]
    exclude = ['necessita_licenciamento_ambiental', 'desativado_por', 'desativado_em']


admin.site.register(models.ProjetoAssentamento, ProjetoAssentamentoAdmin)
admin.site.register(models.Lote, LoteAdmin)
