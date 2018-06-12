from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils import timezone
from datetime import datetime
from django.views import generic
from django.views.generic import ListView, DetailView
from django_tables2 import RequestConfig

from . import models
from . import tables
from . import forms


class LoteListView(ListView):
    model = models.Lote


class LoteDetailView(DetailView):
    model = models.Lote


def listar_contratos(request):
    atualizado_em = datetime.now()
    contratos = models.Contrato.objects.all()
    template_name = 'core/listar_contratos.html'
    context = {
        'contratos': contratos,
        'atualizado_em': atualizado_em
    }
    return render(request, template_name, context)


def listar_projetos_por_contrato(request, contrato_id):
    atualizado_em = datetime.now()
    contrato = models.Contrato.objects.get(pk=contrato_id)
    projetos_assentamento = models.ProjetoAssentamento.objects.filter(contrato=contrato_id)
    template_name = 'core/listar_projetos_assentamento_por_contrato.html'
    context = {
        'projetos_assentamento': projetos_assentamento,
        'contrato': contrato,
        'atualizado_em': atualizado_em
    }
    return render(request, template_name, context)


def listar_diagnosticos_por_projeto_assentamento(request, contrato_id, pa_id):
    atualizado_em = datetime.now()
    projeto_assentamento = models.ProjetoAssentamento.objects.get(pk=pa_id)
    diagnosticos = models.Lote.objects.filter(projeto_assentamento=pa_id)
    template_name = 'core/listar_diagnosticos_por_projeto_assentamento.html'
    context = {
        'diagnosticos': diagnosticos,
        'projeto_assentamento': projeto_assentamento,
        'atualizado_em': atualizado_em

    }
    return render(request, template_name, context)


def listar_projetos_assentamento_por_contrato(request, pk):
    atualizado_em = datetime.now()
    projetos_assentamento = models.ProjetoAssentamento.objects.filter(contrato=pk)
    template_name = 'core/listar_projetos_assentamento_por_contrato.html'
    context = {
        'contratos': projetos_assentamento,
        'atualizado_em': atualizado_em
    }
    return render(request, template_name, context)


def table_view(request):
    template_name = 'core/tabela_exemplo.html'

    lotes_queryset = models.Lote.objects.select_related('projeto_assentamento').all()
    lote_table = tables.LoteTable(lotes_queryset)
    RequestConfig(request).configure(lote_table)
    context = {
        'lote_table': lote_table
    }
    return render(request=request, template_name=template_name, context=context)


class Teste(generic.TemplateView):
    template_name = 'core/datatable_exemplo.html'


def novo_diagnostico(request, pk):
    projeto_assentamento = models.ProjetoAssentamento.objects.only('id', 'contrato_id',).get(pk=pk)

    form = forms.DiagnosticoForm(
        initial={
            'projeto_assentamento': projeto_assentamento.pk
        }
    )

    documentos_lote_forms = forms.DocumentoLoteInlineFormSet(
        prefix='documentos_lote',
        queryset=models.DocumentoLote.objects.none()
    )
    beneficios_forms = forms.BeneficioSocialInlineFormSet(
        prefix='beneficios_sociais',
        queryset=models.BeneficioSocial.objects.none()
    )
    auto_declaracoes_forms = forms.AutoDeclaracaoEtniaInlineFormSet(
        prefix='auto_declaracoes',
        queryset=models.AutoDeclaracaoEtnia.objects.none()
    )
    estruturas_organizativas_forms = forms.EstruturaOrganizativaInlineFormSet(
        prefix='estruturas_organizativas',
        queryset=models.EstruturaOrganizativa.objects.none()
    )

    if request.method == "POST":
        form = forms.DiagnosticoForm(request.POST)
        documentos_lote_forms = forms.DocumentoLoteInlineFormSet(
            request.POST,
            prefix = 'documentos_lote',
            queryset=models.DocumentoLote.objects.none()
        )
        beneficios_forms = forms.BeneficioSocialInlineFormSet(
            request.POST,
            prefix='beneficios_sociais',
            queryset=models.BeneficioSocial.objects.none()
        )
        auto_declaracoes_forms = forms.AutoDeclaracaoEtniaInlineFormSet(
            request.POST,
            prefix='auto_declaracoes',
            queryset=models.AutoDeclaracaoEtnia.objects.none()
        )
        estruturas_organizativas_forms = forms.EstruturaOrganizativaInlineFormSet(
            request.POST,
            prefix='estruturas_organizativas',
            queryset=models.EstruturaOrganizativa.objects.none()
        )

        if form.is_valid() and documentos_lote_forms.is_valid() and beneficios_forms.is_valid() and auto_declaracoes_forms.is_valid() and estruturas_organizativas_forms.is_valid():
            lote = form.save(commit=False)
            lote.save()
            documentos_lote = documentos_lote_forms.save(commit=False)
            for documento in documentos_lote:
                documento.lote = lote
                documento.save()

            beneficios = beneficios_forms.save(commit=False)
            for beneficio in beneficios:
                beneficio.lote = lote
                beneficio.save()

            auto_declaracoes = auto_declaracoes_forms.save(commit=False)
            for auto_declaracao in auto_declaracoes:
                auto_declaracao.lote = lote
                auto_declaracao.save()

            estruturas_organizativas = estruturas_organizativas_forms.save(commit=False)
            for estrutura_organizativa in estruturas_organizativas:
                estrutura_organizativa.lote = lote
                estrutura_organizativa.save()

            template = reverse('core:listar_diagnosticos_por_projeto_assentamento', kwargs={'contrato_id': projeto_assentamento.contrato_id, 'pa_id': projeto_assentamento.pk})
            return redirect(template)
    template_name = 'core/editar_diagnostico.html'
    context = {
        'form': form,
        'DocumentoLoteInlineFormSet': documentos_lote_forms,
        'BeneficioSocialInlineFormSet': beneficios_forms,
        'AutoDeclaracaoEtniaInlineFormSet': auto_declaracoes_forms,
        'EstruturaOrganizativaInlineFormSet': estruturas_organizativas_forms,
        'title': 'Registrar Diagnóstico'
    }
    return render(request, template_name, context)

def novo_diagnostico(request, pa_id):
    projeto_assentamento = models.ProjetoAssentamento.objects.only('id', 'contrato_id',).get(id=pa_id)

    form = forms.DiagnosticoForm(
        initial={
            'projeto_assentamento': projeto_assentamento.pk
        }
    )

    documentos_lote_forms = forms.DocumentoLoteInlineFormSet(
        prefix='documentos_lote',
        queryset=models.DocumentoLote.objects.none()
    )
    beneficios_forms = forms.BeneficioSocialInlineFormSet(
        prefix='beneficios_sociais',
        queryset=models.BeneficioSocial.objects.none()
    )
    auto_declaracoes_forms = forms.AutoDeclaracaoEtniaInlineFormSet(
        prefix='auto_declaracoes',
        queryset=models.AutoDeclaracaoEtnia.objects.none()
    )
    estruturas_organizativas_forms = forms.EstruturaOrganizativaInlineFormSet(
        prefix='estruturas_organizativas',
        queryset=models.EstruturaOrganizativa.objects.none()
    )
    fontes_agua_forms = forms.FonteAguaInlineFormSet(
        prefix='fontes_agua',
        queryset=models.FonteAgua.objects.none()
    )
    tratamentos_agua_forms = forms.TratamentoAguaInlineFormSet(
        prefix='tratamentos_agua',
        queryset=models.TratamentoAgua.objects.none()
    )
    construcoes_lote_forms = forms.ConstrucaoLoteInlineFormSet(
        prefix='construcoes_lote',
        queryset=models.ConstrucaoLote.objects.none()
    )
    bens_produtivos_forms = forms.BemProdutivoInlineFormSet(
        prefix='bens_produtivos',
        queryset=models.BemProdutivo.objects.none()
    )
    aplicacoes_creditos_forms = forms.AplicacaoCreditoInlineFormSet(
        prefix='aplicacoes_creditos',
        queryset=models.AplicacaoCredito.objects.none()
    )
    creditos_bancarios_forms = forms.CreditoBancarioInlineFormSet(
        prefix='creditos_bancarios',
        queryset=models.CreditoBancario.objects.none()
    )

    if request.method == "POST":
        form = forms.DiagnosticoForm(request.POST)
        documentos_lote_forms = forms.DocumentoLoteInlineFormSet(
            request.POST,
            prefix = 'documentos_lote',
            queryset=models.DocumentoLote.objects.none()
        )
        beneficios_forms = forms.BeneficioSocialInlineFormSet(
            request.POST,
            prefix='beneficios_sociais',
            queryset=models.BeneficioSocial.objects.none()
        )
        auto_declaracoes_forms = forms.AutoDeclaracaoEtniaInlineFormSet(
            request.POST,
            prefix='auto_declaracoes',
            queryset=models.AutoDeclaracaoEtnia.objects.none()
        )
        estruturas_organizativas_forms = forms.EstruturaOrganizativaInlineFormSet(
            request.POST,
            prefix='estruturas_organizativas',
            queryset=models.EstruturaOrganizativa.objects.none()
        )
        fontes_agua_forms = forms.FonteAguaInlineFormSet(
            request.POST,
            prefix='fontes_agua',
            queryset=models.FonteAgua.objects.none()
        )
        tratamentos_agua_forms = forms.TratamentoAguaInlineFormSet(
            request.POST,
            prefix='tratamentos_agua',
            queryset=models.TratamentoAgua.objects.none()
        )
        construcoes_lote_forms = forms.ConstrucaoLoteInlineFormSet(
            request.POST,
            prefix='construcoes_lote',
            queryset=models.ConstrucaoLote.objects.none()
        )
        bens_produtivos_forms = forms.BemProdutivoInlineFormSet(
            request.POST,
            prefix='bens_produtivos',
            queryset=models.BemProdutivo.objects.none()
        )
        aplicacoes_creditos_forms = forms.AplicacaoCreditoInlineFormSet(
            request.POST,
            prefix='aplicacoes_creditos',
            queryset=models.AplicacaoCredito.objects.none()
        )
        creditos_bancarios_forms = forms.CreditoBancarioInlineFormSet(
            request.POST,
            prefix='creditos_bancarios',
            queryset=models.CreditoBancario.objects.none()
        )

        if form.is_valid() and documentos_lote_forms.is_valid() and beneficios_forms.is_valid() and auto_declaracoes_forms.is_valid() and estruturas_organizativas_forms.is_valid() and fontes_agua_forms.is_valid() and tratamentos_agua_forms.is_valid() and construcoes_lote_forms.is_valid() and bens_produtivos_forms.is_valid() and aplicacoes_creditos_forms.is_valid() and creditos_bancarios_forms.is_valid():
            lote = form.save(commit=False)
            lote.save()
            documentos_lote = documentos_lote_forms.save(commit=False)
            for documento in documentos_lote:
                documento.lote = lote
                documento.save()

            beneficios = beneficios_forms.save(commit=False)
            for beneficio in beneficios:
                beneficio.lote = lote
                beneficio.save()

            auto_declaracoes = auto_declaracoes_forms.save(commit=False)
            for auto_declaracao in auto_declaracoes:
                auto_declaracao.lote = lote
                auto_declaracao.save()

            estruturas_organizativas = estruturas_organizativas_forms.save(commit=False)
            for estrutura_organizativa in estruturas_organizativas:
                estrutura_organizativa.lote = lote
                estrutura_organizativa.save()

            fontes_agua = fontes_agua_forms.save(commit=False)
            for fonte_agua in fontes_agua:
                fonte_agua.lote = lote
                fonte_agua.save()

            tratamentos_agua = tratamentos_agua_forms.save(commit=False)
            for tratamento_agua in tratamentos_agua:
                tratamento_agua.lote = lote
                tratamento_agua.save()

            construcoes_lote = construcoes_lote_forms.save(commit=False)
            for construcao_lote in construcoes_lote:
                construcao_lote.lote = lote
                construcao_lote.save()

            bens_produtivos = bens_produtivos_forms.save(commit=False)
            for bem_produtivo in bens_produtivos:
                bem_produtivo.lote = lote
                bem_produtivo.save()

            aplicacoes_creditos = aplicacoes_creditos_forms.save(commit=False)
            for aplicacao_credito in aplicacoes_creditos:
                aplicacao_credito.lote = lote
                aplicacao_credito.save()

            creditos_bancarios = creditos_bancarios_forms.save(commit=False)
            for credito_bancario in creditos_bancarios:
                credito_bancario.lote = lote
                credito_bancario.save()

            template = reverse('core:listar_diagnosticos_por_projeto_assentamento', kwargs={'contrato_id': projeto_assentamento.contrato_id, 'pa_id': projeto_assentamento.pk})
            return redirect(template)
    template_name = 'core/editar_diagnostico.html'
    context = {
        'form': form,
        'projeto_assentamento': projeto_assentamento,
        'DocumentoLoteInlineFormSet': documentos_lote_forms,
        'BeneficioSocialInlineFormSet': beneficios_forms,
        'AutoDeclaracaoEtniaInlineFormSet': auto_declaracoes_forms,
        'EstruturaOrganizativaInlineFormSet': estruturas_organizativas_forms,
        'FonteAguaInlineFormSet': fontes_agua_forms,
        'TratamentoAguaInlineFormSet': tratamentos_agua_forms,
        'ConstrucaoLoteInlineFormSet': construcoes_lote_forms,
        'BemProdutivoInlineFormSet': bens_produtivos_forms,
        'AplicacaoCreditoInlineFormSet': aplicacoes_creditos_forms,
        'CreditoBancarioInlineFormSet': creditos_bancarios_forms,
        'title': 'Registrar Diagnóstico'
    }
    return render(request, template_name, context)

def editar_diagnostico(request, pa_id, diagnostico_id):
    diagnostico = get_object_or_404(models.Lote, id=diagnostico_id)
    projeto_assentamento = models.ProjetoAssentamento.objects.only('id', 'contrato_id',).get(id=pa_id)

    form = forms.DiagnosticoForm(
        instance=diagnostico,
        initial={
            'projeto_assentamento': projeto_assentamento.pk
        }
    )

    documentos_lote_forms = forms.DocumentoLoteInlineFormSet(
        prefix='documentos_lote',
        queryset=form.instance.documentos.all()
    )
    beneficios_forms = forms.BeneficioSocialInlineFormSet(
        prefix='beneficios_sociais',
        queryset=form.instance.beneficios.all()
    )
    auto_declaracoes_forms = forms.AutoDeclaracaoEtniaInlineFormSet(
        prefix='auto_declaracoes',
        queryset=form.instance.autoDeclaracoes.all()
    )
    estruturas_organizativas_forms = forms.EstruturaOrganizativaInlineFormSet(
        prefix='estruturas_organizativas',
        queryset=form.instance.estruturasOrganizativas.all()
    )
    fontes_agua_forms = forms.EstruturaOrganizativaInlineFormSet(
        prefix='fontes_agua',
        queryset=form.instance.fontesAgua.all()
    )
    tratamentos_agua_forms = forms.TratamentoAguaInlineFormSet(
        prefix='tratamentos_agua',
        queryset=form.instance.tratamentosAgua.all()
    )
    construcoes_lote_forms = forms.ConstrucaoLoteInlineFormSet(
        prefix='construcoes_lote',
        queryset=form.instance.construcoesLote.all()
    )
    bens_produtivos_forms = forms.BemProdutivoInlineFormSet(
        prefix='bens_produtivos',
        queryset=form.instance.bensProdutivos.all()
    )
    aplicacoes_creditos_forms = forms.AplicacaoCreditoInlineFormSet(
        prefix='aplicacoes_creditos',
        queryset=form.instance.aplicacoesCredito.all()
    )
    creditos_bancarios_forms = forms.CreditoBancarioInlineFormSet(
        prefix='creditos_bancarios',
        queryset=form.instance.creditosBancarios.all()
    )

    if request.method == "POST":
        form = forms.DiagnosticoForm(request.POST)
        documentos_lote_forms = forms.DocumentoLoteInlineFormSet(
            request.POST,
            prefix = 'documentos_lote',
            queryset=form.instance.documentos.all()
        )
        beneficios_forms = forms.BeneficioSocialInlineFormSet(
            request.POST,
            prefix='beneficios_sociais',
            queryset=form.instance.beneficios.all()
        )
        auto_declaracoes_forms = forms.AutoDeclaracaoEtniaInlineFormSet(
            request.POST,
            prefix='auto_declaracoes',
            queryset=form.instance.autoDeclaracoes.all()
        )
        estruturas_organizativas_forms = forms.EstruturaOrganizativaInlineFormSet(
            request.POST,
            prefix='estruturas_organizativas',
            queryset=form.instance.estruturasOrganizativas.all()
        )
        fontes_agua_forms = forms.EstruturaOrganizativaInlineFormSet(
            request.POST,
            prefix='fontes_agua',
            queryset=form.instance.fontesAgua.all()
        )
        tratamentos_agua_forms = forms.TratamentoAguaInlineFormSet(
            request.POST,
            prefix='tratamentos_agua',
            queryset=form.instance.tratamentosAgua.all()
        )
        construcoes_lote_forms = forms.ConstrucaoLoteInlineFormSet(
            request.POST,
            prefix='construcoes_lote',
            queryset=form.instance.construcoesLote.all()
        )
        bens_produtivos_forms = forms.BemProdutivoInlineFormSet(
            request.POST,
            prefix='bens_produtivos',
            queryset=form.instance.bensProdutivos.all()
        )
        aplicacoes_creditos_forms = forms.AplicacaoCreditoInlineFormSet(
            request.POST,
            prefix='aplicacoes_creditos',
            queryset=form.instance.aplicacoesCredito.all()
        )
        creditos_bancarios_forms = forms.CreditoBancarioInlineFormSet(
            request.POST,
            prefix='creditos_bancarios',
            queryset=form.instance.creditosBancarios.all()
        )

        if form.is_valid() and documentos_lote_forms.is_valid() and beneficios_forms.is_valid() and auto_declaracoes_forms.is_valid() and estruturas_organizativas_forms.is_valid() and fontes_agua_forms.is_valid() and tratamentos_agua_forms.is_valid() and construcoes_lote_forms.is_valid() and bens_produtivos_forms.is_valid() and aplicacoes_creditos_forms.is_valid() and creditos_bancarios_forms.is_valid():
            lote = form.save(commit=False)
            lote.save()
            documentos_lote = documentos_lote_forms.save(commit=False)
            for documento in documentos_lote:
                documento.lote = lote
                documento.save()

            beneficios = beneficios_forms.save(commit=False)
            for beneficio in beneficios:
                beneficio.lote = lote
                beneficio.save()

            auto_declaracoes = auto_declaracoes_forms.save(commit=False)
            for auto_declaracao in auto_declaracoes:
                auto_declaracao.lote = lote
                auto_declaracao.save()

            estruturas_organizativas = estruturas_organizativas_forms.save(commit=False)
            for estrutura_organizativa in estruturas_organizativas:
                estrutura_organizativa.lote = lote
                estrutura_organizativa.save()

            fontes_agua = fontes_agua_forms.save(commit=False)
            for fonte_agua in fontes_agua:
                fonte_agua.lote = lote
                fonte_agua.save()

            tratamentos_agua = tratamentos_agua_forms.save(commit=False)
            for tratamento_agua in tratamentos_agua:
                tratamento_agua.lote = lote
                tratamento_agua.save()

            construcoes_lote = construcoes_lote_forms.save(commit=False)
            for construcao_lote in construcoes_lote:
                construcao_lote.lote = lote
                construcao_lote.save()

            bens_produtivos = bens_produtivos_forms.save(commit=False)
            for bem_produtivo in bens_produtivos:
                bem_produtivo.lote = lote
                bem_produtivo.save()

            aplicacoes_creditos = aplicacoes_creditos_forms.save(commit=False)
            for aplicacao_credito in aplicacoes_creditos:
                aplicacao_credito.lote = lote
                aplicacao_credito.save()

            creditos_bancarios = creditos_bancarios_forms.save(commit=False)
            for credito_bancario in creditos_bancarios:
                credito_bancario.lote = lote
                credito_bancario.save()

            template = reverse('core:listar_diagnosticos_por_projeto_assentamento', kwargs={'contrato_id': projeto_assentamento.contrato_id, 'pa_id': projeto_assentamento.pk})
            return redirect(template)
    template_name = 'core/editar_diagnostico.html'
    context = {
        'form': form,
        'projeto_assentamento': projeto_assentamento,
        'DocumentoLoteInlineFormSet': documentos_lote_forms,
        'BeneficioSocialInlineFormSet': beneficios_forms,
        'AutoDeclaracaoEtniaInlineFormSet': auto_declaracoes_forms,
        'EstruturaOrganizativaInlineFormSet': estruturas_organizativas_forms,
        'FonteAguaInlineFormSet': fontes_agua_forms,
        'TratamentoAguaInlineFormSet': tratamentos_agua_forms,
        'ConstrucaoLoteInlineFormSet': construcoes_lote_forms,
        'BemProdutivoInlineFormSet': bens_produtivos_forms,
        'AplicacaoCreditoInlineFormSet': aplicacoes_creditos_forms,
        'CreditoBancarioInlineFormSet': creditos_bancarios_forms,
        'title': 'Editar Diagnóstico'
    }
    return render(request, template_name, context)

# def excluir_diagnostico(request, pa_id, diagnostico_id):
#     diagnostico = get_object_or_404(models.Lote, id=pa_id)
#     projeto_assentamento = models.ProjetoAssentamento.objects.only('id', 'contrato_id', ).get(id=pa_id)
#
#     if request.method == "POST":
#         diagnostico.delete()
#         # messages.success(request, 'Nota de entrada excluída com sucesso!')
#         template = reverse('core:listar_diagnosticos_por_projeto_assentamento',
#                            kwargs={'contrato_id': projeto_assentamento.contrato_id, 'pa_id': projeto_assentamento.pk})
#         return redirect(template)
#     template_name = 'confirmar_acao.html'
#     context = {
#         'objeto': diagnostico,
#         'projeto_assentamento': projeto_assentamento,
#         'title': 'Excluir Diagnóstico',
#         'mensagem': 'Tem certeza que deseja deletar o Diagnóstico: ',
#         'style_button': 'btn btn-danger'
#         # 'diagnostico': True
#     }
#     return render(request, template_name, context)
