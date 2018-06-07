from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from django.views import generic
from django.views.generic import ListView, DetailView
from django_tables2 import RequestConfig

from . import models
from . import tables


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
