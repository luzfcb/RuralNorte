from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils import timezone
from datetime import datetime
from django.views import generic
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django_tables2 import RequestConfig
from django.contrib import messages

from . import models
from . import tables
from . import forms


class BaseUpdateWithInlinesView(SingleObjectMixin, FormView):
    """
    For adding books to a Publisher, or editing them.
    """

    def get(self, request, *args, **kwargs):
        # The Publisher we're editing:
        self.object = self.get_object(queryset=self.get_queryset())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # The Publisher we're uploading for:
        self.object = self.get_object(queryset=self.get_queryset())
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        form.save()

        return HttpResponseRedirect(self.get_success_url())


class LoteListView(ListView):
    model = models.Lote


class LoteDetailView(DetailView):
    model = models.Lote


def login(request):
    template_name = 'core/login.html'
    context = {

    }
    return render(request, template_name, context)


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


def novo_diagnostico(request, pa_id):
    projeto_assentamento = models.ProjetoAssentamento.objects.only('id', 'contrato_id', ).get(id=pa_id)

    form = forms.DiagnosticoForm(
        initial={
            'projeto_assentamento': projeto_assentamento.pk
        }
    )

    membros_forms = forms.MembroInlineFormSet(
        prefix='membros',
        queryset=models.Membro.objects.none()
    )
    contatos_forms = forms.ContatoInlineFormSet(
        prefix='contatos',
        queryset=models.Contato.objects.none()
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
    culturas_forms = forms.CulturaInlineFormSet(
        prefix='culturas',
        queryset=models.Cultura.objects.none()
    )
    olericulturas_forms = forms.OlericulturaInlineFormSet(
        prefix='olericulturas',
        queryset=models.Olericultura.objects.none()
    )
    fruticulturas_forms = forms.FruticulturaInlineFormSet(
        prefix='fruticulturas',
        queryset=models.Fruticultura.objects.none()
    )
    atividades_extrativistas_forms = forms.AtividadeExtrativistaInlineFormSet(
        prefix='atividades_extrativistas',
        queryset=models.AtividadeExtrativista.objects.none()
    )
    producoes_florestais_forms = forms.ProducaoFlorestalInlineFormSet(
        prefix='producoes_florestais',
        queryset=models.ProducaoFlorestal.objects.none()
    )
    bovinoculturas_forms = forms.BovinoculturaInlineFormSet(
        prefix='bovinoculturas',
        queryset=models.Bovinocultura.objects.none()
    )
    outras_criacoes_forms = forms.OutraCriacaoInlineFormSet(
        prefix='outras_criacoes',
        queryset=models.OutraCriacao.objects.none()
    )
    bovinoculturas_leiteira_forms = forms.BovinoculturaLeiteiraInlineFormSet(
        prefix='bovinoculturas_leiteira',
        queryset=models.BovinoculturaLeiteira.objects.none()
    )
    bovinoculturas_corte_forms = forms.BovinoculturaCorteInlineFormSet(
        prefix='bovinoculturas_corte',
        queryset=models.BovinoculturaCorte.objects.none()
    )
    origens_animais_forms = forms.OrigemAnimalInlineFormSet(
        prefix='origens_animais',
        queryset=models.OrigemAnimal.objects.none()
    )
    niveis_tecnologicos_producao_animal_forms = forms.NivelTecnologicoProducaoAnimalInlineFormSet(
        prefix='niveis_tecnologicos_producao_animal',
        queryset=models.NivelTecnologicoProducaoAnimal.objects.none()
    )
    processados_beneficiados_forms = forms.ProcessadoBeneficiadoInlineFormSet(
        prefix='processados_beneficiados',
        queryset=models.ProcessadoBeneficiado.objects.none()
    )
    problemas_ambientais_forms = forms.ProblemaAmbientalInlineFormSet(
        prefix='problemas_ambientais',
        queryset=models.ProblemaAmbiental.objects.none()
    )
    praticas_conservacionistas_forms = forms.PraticaConservacionistaInlineFormSet(
        prefix='praticas_conservacionistas',
        queryset=models.PraticaConservacionista.objects.none()
    )
    licenciamentos_ambientais_forms = forms.LicenciamentoAmbientalInlineFormSet(
        prefix='licenciamentos_ambientais',
        queryset=models.LicenciamentoAmbiental.objects.none()
    )
    atendimento_saude_forms = forms.AtendimentoSaudeForm(
        prefix='atendimento_saude',
        instance=models.AtendimentoSaude()
    )
    programas_saude_forms = forms.ProgramaSaudeInlineFormSet(
        prefix='programas_saude',
        queryset=models.ProgramaSaude.objects.none()
    )
    atividades_fisicas_forms = forms.AtividadeFisicaInlineFormSet(
        prefix='atividades_fisicas',
        queryset=models.AtividadeFisica.objects.none()
    )
    espacos_disponiveis_forms = forms.EspacoDisponivelInlineFormSet(
        prefix='espacos_disponiveis',
        queryset=models.EspacoDisponivel.objects.none()
    )
    estabelecimentos_ensino_forms = forms.EstabelecimentoEnsinoInlineFormSet(
        prefix='estabelecimentos_ensino',
        queryset=models.EstabelecimentoEnsino.objects.none()
    )
    nao_possui_documento_forms = forms.NaoPossuiDocumentoForm(
        prefix='nao_possui_documento',
        instance=models.NaoPossuiDocumento()
    )

    if request.method == "POST":
        inlines = []

        form = forms.DiagnosticoForm(
            request.POST,
            initial={
                'projeto_assentamento': projeto_assentamento.pk
            }
        )

        membros_forms = forms.MembroInlineFormSet(
            request.POST,
            prefix='membros',
            queryset=models.Membro.objects.none()
        )
        inlines.append(membros_forms)

        contatos_forms = forms.ContatoInlineFormSet(
            request.POST,
            prefix='contatos',
            queryset=models.Contato.objects.none()
        )
        inlines.append(contatos_forms)

        documentos_lote_forms = forms.DocumentoLoteInlineFormSet(
            request.POST,
            prefix='documentos_lote',
            queryset=models.DocumentoLote.objects.none()
        )
        inlines.append(documentos_lote_forms)

        beneficios_forms = forms.BeneficioSocialInlineFormSet(
            request.POST,
            prefix='beneficios_sociais',
            queryset=models.BeneficioSocial.objects.none()
        )
        inlines.append(beneficios_forms)

        auto_declaracoes_forms = forms.AutoDeclaracaoEtniaInlineFormSet(
            request.POST,
            prefix='auto_declaracoes',
            queryset=models.AutoDeclaracaoEtnia.objects.none()
        )
        inlines.append(auto_declaracoes_forms)

        estruturas_organizativas_forms = forms.EstruturaOrganizativaInlineFormSet(
            request.POST,
            prefix='estruturas_organizativas',
            queryset=models.EstruturaOrganizativa.objects.none()
        )
        inlines.append(estruturas_organizativas_forms)

        fontes_agua_forms = forms.FonteAguaInlineFormSet(
            request.POST,
            prefix='fontes_agua',
            queryset=models.FonteAgua.objects.none()
        )
        inlines.append(fontes_agua_forms)

        tratamentos_agua_forms = forms.TratamentoAguaInlineFormSet(
            request.POST,
            prefix='tratamentos_agua',
            queryset=models.TratamentoAgua.objects.none()
        )
        inlines.append(tratamentos_agua_forms)

        construcoes_lote_forms = forms.ConstrucaoLoteInlineFormSet(
            request.POST,
            prefix='construcoes_lote',
            queryset=models.ConstrucaoLote.objects.none()
        )
        inlines.append(construcoes_lote_forms)

        bens_produtivos_forms = forms.BemProdutivoInlineFormSet(
            request.POST,
            prefix='bens_produtivos',
            queryset=models.BemProdutivo.objects.none()
        )
        inlines.append(bens_produtivos_forms)

        aplicacoes_creditos_forms = forms.AplicacaoCreditoInlineFormSet(
            request.POST,
            prefix='aplicacoes_creditos',
            queryset=models.AplicacaoCredito.objects.none()
        )
        inlines.append(aplicacoes_creditos_forms)

        creditos_bancarios_forms = forms.CreditoBancarioInlineFormSet(
            request.POST,
            prefix='creditos_bancarios',
            queryset=models.CreditoBancario.objects.none()
        )
        inlines.append(creditos_bancarios_forms)

        culturas_forms = forms.CulturaInlineFormSet(
            request.POST,
            prefix='culturas',
            queryset=models.Cultura.objects.none()
        )
        inlines.append(culturas_forms)

        olericulturas_forms = forms.OlericulturaInlineFormSet(
            request.POST,
            prefix='olericulturas',
            queryset=models.Olericultura.objects.none()
        )
        inlines.append(olericulturas_forms)

        fruticulturas_forms = forms.FruticulturaInlineFormSet(
            request.POST,
            prefix='fruticulturas',
            queryset=models.Fruticultura.objects.none()
        )
        inlines.append(fruticulturas_forms)

        atividades_extrativistas_forms = forms.AtividadeExtrativistaInlineFormSet(
            request.POST,
            prefix='atividades_extrativistas',
            queryset=models.AtividadeExtrativista.objects.none()
        )
        inlines.append(atividades_extrativistas_forms)

        producoes_florestais_forms = forms.ProducaoFlorestalInlineFormSet(
            request.POST,
            prefix='producoes_florestais',
            queryset=models.ProducaoFlorestal.objects.none()
        )
        inlines.append(producoes_florestais_forms)

        bovinoculturas_forms = forms.BovinoculturaInlineFormSet(
            request.POST,
            prefix='bovinoculturas',
            queryset=models.Bovinocultura.objects.none()
        )
        inlines.append(bovinoculturas_forms)

        outras_criacoes_forms = forms.OutraCriacaoInlineFormSet(
            request.POST,
            prefix='outras_criacoes',
            queryset=models.OutraCriacao.objects.none()
        )
        inlines.append(outras_criacoes_forms)

        bovinoculturas_leiteira_forms = forms.BovinoculturaLeiteiraInlineFormSet(
            request.POST,
            prefix='bovinoculturas_leiteira',
            queryset=models.BovinoculturaLeiteira.objects.none()
        )
        inlines.append(bovinoculturas_leiteira_forms)

        bovinoculturas_corte_forms = forms.BovinoculturaCorteInlineFormSet(
            request.POST,
            prefix='bovinoculturas_corte',
            queryset=models.BovinoculturaCorte.objects.none()
        )
        inlines.append(bovinoculturas_corte_forms)

        origens_animais_forms = forms.OrigemAnimalInlineFormSet(
            request.POST,
            prefix='origens_animais',
            queryset=models.OrigemAnimal.objects.none()
        )
        inlines.append(origens_animais_forms)

        niveis_tecnologicos_producao_animal_forms = forms.NivelTecnologicoProducaoAnimalInlineFormSet(
            request.POST,
            prefix='niveis_tecnologicos_producao_animal',
            queryset=models.NivelTecnologicoProducaoAnimal.objects.none()
        )
        inlines.append(niveis_tecnologicos_producao_animal_forms)

        processados_beneficiados_forms = forms.ProcessadoBeneficiadoInlineFormSet(
            request.POST,
            prefix='processados_beneficiados',
            queryset=models.ProcessadoBeneficiado.objects.none()
        )
        inlines.append(processados_beneficiados_forms)

        problemas_ambientais_forms = forms.ProblemaAmbientalInlineFormSet(
            request.POST,
            prefix='problemas_ambientais',
            queryset=models.ProblemaAmbiental.objects.none()
        )
        inlines.append(problemas_ambientais_forms)

        praticas_conservacionistas_forms = forms.PraticaConservacionistaInlineFormSet(
            request.POST,
            prefix='praticas_conservacionistas',
            queryset=models.PraticaConservacionista.objects.none()
        )
        inlines.append(praticas_conservacionistas_forms)

        licenciamentos_ambientais_forms = forms.LicenciamentoAmbientalInlineFormSet(
            request.POST,
            prefix='licenciamentos_ambientais',
            queryset=models.LicenciamentoAmbiental.objects.none()
        )
        inlines.append(licenciamentos_ambientais_forms)

        atendimento_saude_forms = forms.AtendimentoSaudeForm(
            request.POST,
            prefix='atendimento_saude',
            instance=models.AtendimentoSaude()
        )

        programas_saude_forms = forms.ProgramaSaudeInlineFormSet(
            request.POST,
            prefix='programas_saude',
            queryset=models.ProgramaSaude.objects.none()
        )
        inlines.append(programas_saude_forms)

        atividades_fisicas_forms = forms.AtividadeFisicaInlineFormSet(
            request.POST,
            prefix='atividades_fisicas',
            queryset=models.AtividadeFisica.objects.none()
        )
        inlines.append(atividades_fisicas_forms)

        espacos_disponiveis_forms = forms.EspacoDisponivelInlineFormSet(
            request.POST,
            prefix='espacos_disponiveis',
            queryset=models.EspacoDisponivel.objects.none()
        )
        inlines.append(espacos_disponiveis_forms)

        estabelecimentos_ensino_forms = forms.EstabelecimentoEnsinoInlineFormSet(
            request.POST,
            prefix='estabelecimentos_ensino',
            queryset=models.EstabelecimentoEnsino.objects.none()
        )
        inlines.append(estabelecimentos_ensino_forms)

        nao_possui_documento_forms = forms.NaoPossuiDocumentoForm(
            request.POST,
            prefix='nao_possui_documento',
            instance=models.NaoPossuiDocumento()
        )

        if form.is_valid() and atendimento_saude_forms.is_valid() and nao_possui_documento_forms.is_valid() \
            and all([item.is_valid() for item in inlines]):

            lote = form.save(commit=False)
            lote.save()

            for form in inlines:
                inline = form.save(commit=False)

                for item in inline:
                    item.lote = lote
                    item.save()

            atendimento_saude = atendimento_saude_forms.save(commit=False)
            atendimento_saude.lote = lote
            atendimento_saude.save()

            nao_possui_documento = nao_possui_documento_forms.save(commit=False)
            nao_possui_documento.lote = lote
            nao_possui_documento.save()

            template = reverse('core:listar_diagnosticos_por_projeto_assentamento',
                               kwargs={'contrato_id': projeto_assentamento.contrato_id,
                                       'pa_id': projeto_assentamento.pk})
            messages.success(request, 'Diagnóstico salvo com sucesso!')
            return redirect(template)
    template_name = 'core/editar_diagnostico.html'
    context = {
        'form': form,
        'projeto_assentamento': projeto_assentamento,
        'MembroInlineFormSet': membros_forms,
        'ContatoInlineFormSet': contatos_forms,
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
        'CulturaInlineFormSet': culturas_forms,
        'OlericulturaInlineFormSet': olericulturas_forms,
        'FruticulturaInlineFormSet': fruticulturas_forms,
        'AtividadeExtrativistaInlineFormSet': atividades_extrativistas_forms,
        'ProducaoFlorestalInlineFormSet': producoes_florestais_forms,
        'BovinoculturaInlineFormSet': bovinoculturas_forms,
        'OutraCriacaoInlineFormSet': outras_criacoes_forms,
        'BovinoculturaLeiteiraInlineFormSet': bovinoculturas_leiteira_forms,
        'BovinoculturaCorteInlineFormSet': bovinoculturas_corte_forms,
        'OrigemAnimalInlineFormSet': origens_animais_forms,
        'NivelTecnologicoProducaoAnimalInlineFormSet': niveis_tecnologicos_producao_animal_forms,
        'ProcessadoBeneficiadoInlineFormSet': processados_beneficiados_forms,
        'ProblemaAmbientalInlineFormSet': problemas_ambientais_forms,
        'PraticaConservacionistaInlineFormSet': praticas_conservacionistas_forms,
        'LicenciamentoAmbientalInlineFormSet': licenciamentos_ambientais_forms,
        'AtendimentoSaudeForm': atendimento_saude_forms,
        'ProgramaSaudeInlineFormSet': programas_saude_forms,
        'AtividadeFisicaInlineFormSet': atividades_fisicas_forms,
        'EspacoDisponivelInlineFormSet': espacos_disponiveis_forms,
        'EstabelecimentoEnsinoInlineFormSet': estabelecimentos_ensino_forms,
        'NaoPossuiDocumentoForm': nao_possui_documento_forms,
        'title': 'Registrar Diagnóstico'
    }
    return render(request, template_name, context)


def editar_diagnostico(request, pa_id, diagnostico_id):
    diagnostico = get_object_or_404(models.Lote, id=diagnostico_id)
    projeto_assentamento = models.ProjetoAssentamento.objects.only('id', 'contrato_id', ).get(id=pa_id)

    form = forms.DiagnosticoForm(
        instance=diagnostico,
        initial={
            'projeto_assentamento': projeto_assentamento.pk
        }
    )

    membros_forms = forms.MembroInlineFormSet(
        prefix='membros',
        queryset=form.instance.membros.all()
    )
    contatos_forms = forms.ContatoInlineFormSet(
        prefix='contatos',
        queryset=form.instance.contatos.all()
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
    fontes_agua_forms = forms.FonteAguaInlineFormSet(
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
    culturas_forms = forms.CulturaInlineFormSet(
        prefix='culturas',
        queryset=form.instance.producoesVegetais.filter(classificacao=models.Cultura.CLASSIFICACAO_CULTURA)
    )
    olericulturas_forms = forms.OlericulturaInlineFormSet(
        prefix='olericulturas',
        queryset=form.instance.producoesVegetais.filter(classificacao=models.Cultura.CLASSIFICACAO_OLERICULTURA)
    )
    fruticulturas_forms = forms.FruticulturaInlineFormSet(
        prefix='fruticulturas',
        queryset=form.instance.producoesVegetais.filter(classificacao=models.Cultura.CLASSIFICACAO_FRUTICULTURA)
    )
    atividades_extrativistas_forms = forms.AtividadeExtrativistaInlineFormSet(
        prefix='atividades_extrativistas',
        queryset=form.instance.atividadesExtrativistas.all()
    )
    producoes_florestais_forms = forms.ProducaoFlorestalInlineFormSet(
        prefix='producoes_florestais',
        queryset=form.instance.producoesFlorestais.all()
    )
    bovinoculturas_forms = forms.BovinoculturaInlineFormSet(
        prefix='bovinoculturas',
        queryset=form.instance.producoesAnimais.filter(classificacao=models.Bovinocultura.CLASSIFICACAO_BOVINOCULTURA)
    )
    outras_criacoes_forms = forms.OutraCriacaoInlineFormSet(
        prefix='outras_criacoes',
        queryset=form.instance.producoesAnimais.filter(classificacao=models.Bovinocultura.CLASSIFICACAO_OUTRA_CRIACAO)
    )
    bovinoculturas_leiteira_forms = forms.BovinoculturaLeiteiraInlineFormSet(
        prefix='bovinoculturas_leiteira',
        queryset=form.instance.descartesAnimais.filter(
            tipo_criacao=models.BovinoculturaLeiteira.TIPO_CRIACAO_GADO_LEITEIRO)
    )
    bovinoculturas_corte_forms = forms.BovinoculturaCorteInlineFormSet(
        prefix='bovinoculturas_corte',
        queryset=form.instance.descartesAnimais.filter(
            tipo_criacao=models.BovinoculturaCorte.TIPO_CRIACAO_GADO_DE_CORTE)
    )
    origens_animais_forms = forms.OrigemAnimalInlineFormSet(
        prefix='origens_animais',
        queryset=form.instance.produtosOrigemAnimal.filter(
            classificacao=models.OrigemAnimal.CLASSIFICACAO_ORIGEM_ANIMAL)
    )
    niveis_tecnologicos_producao_animal_forms = forms.NivelTecnologicoProducaoAnimalInlineFormSet(
        prefix='niveis_tecnologicos_producao_animal',
        queryset=form.instance.niveisTecnologicosProducaoAnimal.all()
    )
    processados_beneficiados_forms = forms.ProcessadoBeneficiadoInlineFormSet(
        prefix='processados_beneficiados',
        queryset=form.instance.produtosOrigemAnimal.filter(
            classificacao=models.ProcessadoBeneficiado.CLASSIFICACAO_PROCESSADO_BENEFICIADO)
    )
    problemas_ambientais_forms = forms.ProblemaAmbientalInlineFormSet(
        prefix='problemas_ambientais',
        queryset=form.instance.problemasAmbientais.all()
    )
    praticas_conservacionistas_forms = forms.PraticaConservacionistaInlineFormSet(
        prefix='praticas_conservacionistas',
        queryset=form.instance.praticasConservacionistas.all()
    )
    licenciamentos_ambientais_forms = forms.LicenciamentoAmbientalInlineFormSet(
        prefix='licenciamentos_ambientais',
        queryset=form.instance.licenciamentosAmbientais.all()
    )
    atendimento_saude_forms = forms.AtendimentoSaudeForm(
        prefix='atendimento_saude',
        instance=form.instance.atendimentosSaude
    )
    programas_saude_forms = forms.ProgramaSaudeInlineFormSet(
        prefix='programas_saude',
        queryset=form.instance.programasSaude.all()
    )
    atividades_fisicas_forms = forms.AtividadeFisicaInlineFormSet(
        prefix='atividades_fisicas',
        queryset=form.instance.atividadesFisicas.all()
    )
    espacos_disponiveis_forms = forms.EspacoDisponivelInlineFormSet(
        prefix='espacos_disponiveis',
        queryset=form.instance.espacosDisponiveis.all()
    )
    estabelecimentos_ensino_forms = forms.EstabelecimentoEnsinoInlineFormSet(
        prefix='estabelecimentos_ensino',
        queryset=form.instance.estabelecimentosEnsino.all()
    )
    nao_possui_documento_forms = forms.NaoPossuiDocumentoForm(
        prefix='nao_possui_documento',
        instance=form.instance.nao_possui_documento
    )

    if request.method == "POST":
        inlines = []

        form = forms.DiagnosticoForm(
            request.POST,
            instance=diagnostico,
            initial={
                'projeto_assentamento': projeto_assentamento.pk
            }
        )

        membros_forms = forms.MembroInlineFormSet(
            request.POST,
            prefix='membros',
            queryset=form.instance.membros.all()
        )
        inlines.append(membros_forms)

        contatos_forms = forms.ContatoInlineFormSet(
            request.POST,
            prefix='contatos',
            queryset=form.instance.contatos.all()
        )
        inlines.append(contatos_forms)

        documentos_lote_forms = forms.DocumentoLoteInlineFormSet(
            request.POST,
            prefix='documentos_lote',
            queryset=form.instance.documentos.all()
        )
        inlines.append(documentos_lote_forms)

        beneficios_forms = forms.BeneficioSocialInlineFormSet(
            request.POST,
            prefix='beneficios_sociais',
            queryset=form.instance.beneficios.all()
        )
        inlines.append(beneficios_forms)

        auto_declaracoes_forms = forms.AutoDeclaracaoEtniaInlineFormSet(
            request.POST,
            prefix='auto_declaracoes',
            queryset=form.instance.autoDeclaracoes.all()
        )
        inlines.append(auto_declaracoes_forms)

        estruturas_organizativas_forms = forms.EstruturaOrganizativaInlineFormSet(
            request.POST,
            prefix='estruturas_organizativas',
            queryset=form.instance.estruturasOrganizativas.all()
        )
        inlines.append(estruturas_organizativas_forms)

        fontes_agua_forms = forms.FonteAguaInlineFormSet(
            request.POST,
            prefix='fontes_agua',
            queryset=form.instance.fontesAgua.all()
        )
        inlines.append(fontes_agua_forms)

        tratamentos_agua_forms = forms.TratamentoAguaInlineFormSet(
            request.POST,
            prefix='tratamentos_agua',
            queryset=form.instance.tratamentosAgua.all()
        )
        inlines.append(tratamentos_agua_forms)

        construcoes_lote_forms = forms.ConstrucaoLoteInlineFormSet(
            request.POST,
            prefix='construcoes_lote',
            queryset=form.instance.construcoesLote.all()
        )
        inlines.append(construcoes_lote_forms)

        bens_produtivos_forms = forms.BemProdutivoInlineFormSet(
            request.POST,
            prefix='bens_produtivos',
            queryset=form.instance.bensProdutivos.all()
        )
        inlines.append(bens_produtivos_forms)

        aplicacoes_creditos_forms = forms.AplicacaoCreditoInlineFormSet(
            request.POST,
            prefix='aplicacoes_creditos',
            queryset=form.instance.aplicacoesCredito.all()
        )
        inlines.append(aplicacoes_creditos_forms)

        creditos_bancarios_forms = forms.CreditoBancarioInlineFormSet(
            request.POST,
            prefix='creditos_bancarios',
            queryset=form.instance.creditosBancarios.all()
        )
        inlines.append(creditos_bancarios_forms)

        culturas_forms = forms.CulturaInlineFormSet(
            request.POST,
            prefix='culturas',
            queryset=form.instance.producoesVegetais.filter(classificacao=models.Cultura.CLASSIFICACAO_CULTURA)
        )
        inlines.append(culturas_forms)

        olericulturas_forms = forms.OlericulturaInlineFormSet(
            request.POST,
            prefix='olericulturas',
            queryset=form.instance.producoesVegetais.filter(classificacao=models.Cultura.CLASSIFICACAO_OLERICULTURA)
        )
        inlines.append(olericulturas_forms)

        fruticulturas_forms = forms.FruticulturaInlineFormSet(
            request.POST,
            prefix='fruticulturas',
            queryset=form.instance.producoesVegetais.filter(classificacao=models.Cultura.CLASSIFICACAO_FRUTICULTURA)
        )
        inlines.append(fruticulturas_forms)

        atividades_extrativistas_forms = forms.AtividadeExtrativistaInlineFormSet(
            request.POST,
            prefix='atividades_extrativistas',
            queryset=form.instance.atividadesExtrativistas.all()
        )
        inlines.append(atividades_extrativistas_forms)

        producoes_florestais_forms = forms.ProducaoFlorestalInlineFormSet(
            request.POST,
            prefix='producoes_florestais',
            queryset=form.instance.producoesFlorestais.all()
        )
        inlines.append(producoes_florestais_forms)

        bovinoculturas_forms = forms.BovinoculturaInlineFormSet(
            request.POST,
            prefix='bovinoculturas',
            queryset=form.instance.producoesAnimais.filter(
                classificacao=models.Bovinocultura.CLASSIFICACAO_BOVINOCULTURA)
        )
        inlines.append(bovinoculturas_forms)

        outras_criacoes_forms = forms.OutraCriacaoInlineFormSet(
            request.POST,
            prefix='outras_criacoes',
            queryset=form.instance.producoesAnimais.filter(
                classificacao=models.Bovinocultura.CLASSIFICACAO_OUTRA_CRIACAO)
        )
        inlines.append(outras_criacoes_forms)

        bovinoculturas_leiteira_forms = forms.BovinoculturaLeiteiraInlineFormSet(
            request.POST,
            prefix='bovinoculturas_leiteira',
            queryset=form.instance.descartesAnimais.filter(
                tipo_criacao=models.BovinoculturaLeiteira.TIPO_CRIACAO_GADO_LEITEIRO)
        )
        inlines.append(bovinoculturas_leiteira_forms)

        bovinoculturas_corte_forms = forms.BovinoculturaCorteInlineFormSet(
            request.POST,
            prefix='bovinoculturas_corte',
            queryset=form.instance.descartesAnimais.filter(
                tipo_criacao=models.BovinoculturaCorte.TIPO_CRIACAO_GADO_DE_CORTE)
        )
        inlines.append(bovinoculturas_corte_forms)

        origens_animais_forms = forms.OrigemAnimalInlineFormSet(
            request.POST,
            prefix='origens_animais',
            queryset=form.instance.produtosOrigemAnimal.filter(
                classificacao=models.OrigemAnimal.CLASSIFICACAO_ORIGEM_ANIMAL)
        )
        inlines.append(origens_animais_forms)

        niveis_tecnologicos_producao_animal_forms = forms.NivelTecnologicoProducaoAnimalInlineFormSet(
            request.POST,
            prefix='niveis_tecnologicos_producao_animal',
            queryset=form.instance.niveisTecnologicosProducaoAnimal.all()
        )
        inlines.append(niveis_tecnologicos_producao_animal_forms)

        processados_beneficiados_forms = forms.ProcessadoBeneficiadoInlineFormSet(
            request.POST,
            prefix='processados_beneficiados',
            queryset=form.instance.produtosOrigemAnimal.filter(
                classificacao=models.ProcessadoBeneficiado.CLASSIFICACAO_PROCESSADO_BENEFICIADO)
        )
        inlines.append(processados_beneficiados_forms)

        problemas_ambientais_forms = forms.ProblemaAmbientalInlineFormSet(
            request.POST,
            prefix='problemas_ambientais',
            queryset=form.instance.problemasAmbientais.all()
        )
        inlines.append(problemas_ambientais_forms)

        praticas_conservacionistas_forms = forms.PraticaConservacionistaInlineFormSet(
            request.POST,
            prefix='praticas_conservacionistas',
            queryset=form.instance.praticasConservacionistas.all()
        )
        inlines.append(praticas_conservacionistas_forms)

        licenciamentos_ambientais_forms = forms.LicenciamentoAmbientalInlineFormSet(
            request.POST,
            prefix='licenciamentos_ambientais',
            queryset=form.instance.licenciamentosAmbientais.all()
        )
        inlines.append(licenciamentos_ambientais_forms)

        atendimento_saude_forms = forms.AtendimentoSaudeForm(
            request.POST,
            prefix='atendimento_saude',
            instance=form.instance.atendimentosSaude
        )

        programas_saude_forms = forms.ProgramaSaudeInlineFormSet(
            request.POST,
            prefix='programas_saude',
            queryset=form.instance.programasSaude.all()
        )
        inlines.append(programas_saude_forms)

        atividades_fisicas_forms = forms.AtividadeFisicaInlineFormSet(
            request.POST,
            prefix='atividades_fisicas',
            queryset=form.instance.atividadesFisicas.all()
        )
        inlines.append(atividades_fisicas_forms)

        espacos_disponiveis_forms = forms.EspacoDisponivelInlineFormSet(
            request.POST,
            prefix='espacos_disponiveis',
            queryset=form.instance.espacosDisponiveis.all()
        )
        inlines.append(espacos_disponiveis_forms)

        estabelecimentos_ensino_forms = forms.EstabelecimentoEnsinoInlineFormSet(
            request.POST,
            prefix='estabelecimentos_ensino',
            queryset=form.instance.estabelecimentosEnsino.all()
        )
        inlines.append(estabelecimentos_ensino_forms)

        nao_possui_documento_forms = forms.NaoPossuiDocumentoForm(
            request.POST,
            prefix='nao_possui_documento',
            instance=form.instance.nao_possui_documento
        )

        if form.is_valid() and atendimento_saude_forms.is_valid() and nao_possui_documento_forms.is_valid() \
            and all([item.is_valid() for item in inlines]):

            lote = form.save(commit=False)
            lote.save()

            for form in inlines:
                inline = form.save(commit=False)
                inline_delete = form.deleted_objects

                for item in inline:
                    item.lote = lote
                    item.save()

                for item in inline_delete:
                    item.delete()

            atendimento_saude = atendimento_saude_forms.save(commit=False)
            atendimento_saude.lote = lote
            atendimento_saude.save()

            nao_possui_documento = nao_possui_documento_forms.save(commit=False)
            nao_possui_documento.lote = lote
            nao_possui_documento.save()

            template = reverse('core:listar_diagnosticos_por_projeto_assentamento',
                               kwargs={'contrato_id': projeto_assentamento.contrato_id,
                                       'pa_id': projeto_assentamento.pk})
            messages.success(request, 'Diagnóstico alterado com sucesso!')
            return redirect(template)
    template_name = 'core/editar_diagnostico.html'
    context = {
        'form': form,
        'projeto_assentamento': projeto_assentamento,
        'MembroInlineFormSet': membros_forms,
        'ContatoInlineFormSet': contatos_forms,
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
        'CulturaInlineFormSet': culturas_forms,
        'OlericulturaInlineFormSet': olericulturas_forms,
        'FruticulturaInlineFormSet': fruticulturas_forms,
        'AtividadeExtrativistaInlineFormSet': atividades_extrativistas_forms,
        'ProducaoFlorestalInlineFormSet': producoes_florestais_forms,
        'BovinoculturaInlineFormSet': bovinoculturas_forms,
        'OutraCriacaoInlineFormSet': outras_criacoes_forms,
        'BovinoculturaLeiteiraInlineFormSet': bovinoculturas_leiteira_forms,
        'BovinoculturaCorteInlineFormSet': bovinoculturas_corte_forms,
        'OrigemAnimalInlineFormSet': origens_animais_forms,
        'NivelTecnologicoProducaoAnimalInlineFormSet': niveis_tecnologicos_producao_animal_forms,
        'ProcessadoBeneficiadoInlineFormSet': processados_beneficiados_forms,
        'ProblemaAmbientalInlineFormSet': problemas_ambientais_forms,
        'PraticaConservacionistaInlineFormSet': praticas_conservacionistas_forms,
        'LicenciamentoAmbientalInlineFormSet': licenciamentos_ambientais_forms,
        'AtendimentoSaudeForm': atendimento_saude_forms,
        'ProgramaSaudeInlineFormSet': programas_saude_forms,
        'AtividadeFisicaInlineFormSet': atividades_fisicas_forms,
        'EspacoDisponivelInlineFormSet': espacos_disponiveis_forms,
        'EstabelecimentoEnsinoInlineFormSet': estabelecimentos_ensino_forms,
        'NaoPossuiDocumentoForm': nao_possui_documento_forms,
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
