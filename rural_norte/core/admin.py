from django.contrib import admin

from . import models
from django.template.defaultfilters import date


class ContratoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'ano', 'cadastrado_em')
    search_fields = ['numero', 'ano']
    list_filter = ['ano', 'cadastrado_em']
    exclude = ['desativado_por', 'desativado_em']


class ProjetoAssentamentoAdmin(admin.ModelAdmin):

    def get_data_criacao(self, obj):
        return date(obj.data_criacao, 'd/m/Y')

    get_data_criacao.admin_order_field = 'data_criacao'
    get_data_criacao.short_description = 'Data de Criação'

    def get_total_beneficiarios(self, obj):
        return obj.lotes.count()

    get_total_beneficiarios.short_description = 'Total de Beneficiários'

    list_display = ('codigo', 'nome', 'municipio', 'contrato', 'get_data_criacao', 'get_total_beneficiarios', 'capacidade_projeto')
    search_fields = ['codigo', 'nome', 'municipio']
    list_filter = ['contrato', 'municipio', 'cadastrado_em', 'modificado_em']
    exclude = ['desativado_por', 'desativado_em']


admin.site.register(models.Contrato, ContratoAdmin)
admin.site.register(models.ProjetoAssentamento, ProjetoAssentamentoAdmin)
admin.site.disable_action('delete_selected')
