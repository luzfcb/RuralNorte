from django.shortcuts import render, redirect
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


def novo_diagnostico(request):
    form = forms.DiagnosticoForm()
    documentos_lote_forms = forms.DocumentoLoteInlineFormSet(
        queryset=models.DocumentoLote.objects.none()
    )

    if request.method == "POST":
        form = forms.DiagnosticoForm(request.POST)
        documentos_lote_forms = forms.DocumentoLoteInlineFormSet(
            request.POST,
            queryset=models.DocumentoLote.objects.none()
        )

        if form.is_valid() and documentos_lote_forms.is_valid():
            lote = form.save(commit=False)
            lote.save()
            documentos_lote = documentos_lote_forms.save(commit=False)
            for documento in documentos_lote:
                documento.lote = lote
                documento.save()
            return redirect('core:listar_contratos')
    template_name = 'core/editar_diagnostico.html'
    context = {
        'form': form,
        'formset': documentos_lote_forms,
        'title': 'Registrar Diagnóstico'
    }
    return render(request, template_name, context)
