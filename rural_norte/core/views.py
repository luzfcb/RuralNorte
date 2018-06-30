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


def novo_diagnostico(request, pa_id):
    projeto_assentamento = models.ProjetoAssentamento.objects.only('id', 'contrato_id', ).get(id=pa_id)

    form = forms.DiagnosticoForm(
        initial={
            'projeto_assentamento': projeto_assentamento.pk
        }
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

    if request.method == "POST":
        form = forms.DiagnosticoForm(
            request.POST,
            initial={
                'projeto_assentamento': projeto_assentamento.pk
            }
        )

        contatos_forms = forms.ContatoInlineFormSet(
            request.POST,
            prefix='contatos',
            queryset=models.Contato.objects.none()
        )
        documentos_lote_forms = forms.DocumentoLoteInlineFormSet(
            request.POST,
            prefix='documentos_lote',
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
        culturas_forms = forms.CulturaInlineFormSet(
            request.POST,
            prefix='culturas',
            queryset=models.Cultura.objects.none()
        )
        olericulturas_forms = forms.OlericulturaInlineFormSet(
            request.POST,
            prefix='olericulturas',
            queryset=models.Olericultura.objects.none()
        )
        fruticulturas_forms = forms.FruticulturaInlineFormSet(
            request.POST,
            prefix='fruticulturas',
            queryset=models.Fruticultura.objects.none()
        )
        atividades_extrativistas_forms = forms.AtividadeExtrativistaInlineFormSet(
            request.POST,
            prefix='atividades_extrativistas',
            queryset=models.AtividadeExtrativista.objects.none()
        )
        producoes_florestais_forms = forms.ProducaoFlorestalInlineFormSet(
            request.POST,
            prefix='producoes_florestais',
            queryset=models.ProducaoFlorestal.objects.none()
        )
        bovinoculturas_forms = forms.BovinoculturaInlineFormSet(
            request.POST,
            prefix='bovinoculturas',
            queryset=models.Bovinocultura.objects.none()
        )
        outras_criacoes_forms = forms.OutraCriacaoInlineFormSet(
            request.POST,
            prefix='outras_criacoes',
            queryset=models.OutraCriacao.objects.none()
        )
        bovinoculturas_leiteira_forms = forms.BovinoculturaLeiteiraInlineFormSet(
            request.POST,
            prefix='bovinoculturas_leiteira',
            queryset=models.BovinoculturaLeiteira.objects.none()
        )
        bovinoculturas_corte_forms = forms.BovinoculturaCorteInlineFormSet(
            request.POST,
            prefix='bovinoculturas_corte',
            queryset=models.BovinoculturaCorte.objects.none()
        )
        origens_animais_forms = forms.OrigemAnimalInlineFormSet(
            request.POST,
            prefix='origens_animais',
            queryset=models.OrigemAnimal.objects.none()
        )
        niveis_tecnologicos_producao_animal_forms = forms.NivelTecnologicoProducaoAnimalInlineFormSet(
            prefix='niveis_tecnologicos_producao_animal',
            queryset=models.NivelTecnologicoProducaoAnimal.objects.none()
        )
        processados_beneficiados_forms = forms.ProcessadoBeneficiadoInlineFormSet(
            request.POST,
            prefix='processados_beneficiados',
            queryset=models.ProcessadoBeneficiado.objects.none()
        )

        # if form.is_valid() and documentos_lote_forms.is_valid() and beneficios_forms.is_valid() \
        #     and auto_declaracoes_forms.is_valid() and estruturas_organizativas_forms.is_valid() \
        #     and fontes_agua_forms.is_valid() and tratamentos_agua_forms.is_valid() and construcoes_lote_forms.is_valid() \
        #     and bens_produtivos_forms.is_valid() and aplicacoes_creditos_forms.is_valid() \
        #     and creditos_bancarios_forms.is_valid() and culturas_forms.is_valid() and olericulturas_forms.is_valid() \
        #     and fruticulturas_forms.is_valid() and atividades_extrativistas_forms.is_valid() \
        #     and producoes_florestais_forms.is_valid() and bovinoculturas_forms.is_valid() \
        #     and outras_criacoes_forms.is_valid() and bovinoculturas_leiteira_forms.is_valid() \
        #     and bovinoculturas_corte_forms.is_valid() and origens_animais_forms.is_valid() \
        #     and niveis_tecnologicos_producao_animal_forms.is_valid() and processados_beneficiados_forms.is_valid():
        if (
            form.is_valid() and contatos_forms.is_valid() and documentos_lote_forms.is_valid() and beneficios_forms.is_valid()
            and auto_declaracoes_forms.is_valid() and estruturas_organizativas_forms.is_valid()
            and fontes_agua_forms.is_valid() and tratamentos_agua_forms.is_valid() and construcoes_lote_forms.is_valid()
            and bens_produtivos_forms.is_valid() and aplicacoes_creditos_forms.is_valid()
            and creditos_bancarios_forms.is_valid() and culturas_forms.is_valid()):
            lote = form.save(commit=False)
            lote.save()

            contatos = contatos_forms.save(commit=False)
            for contato in contatos:
                contato.lote = lote
                contato.save()

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

            culturas = culturas_forms.save(commit=False)
            for cultura in culturas:
                cultura.classificacao = models.Cultura.CLASSIFICACAO_CULTURA
                cultura.lote = lote
                cultura.save()

            # olericulturas = olericulturas_forms.save(commit=False)
            # for olericultura in olericulturas:
            #     olericultura.lote = lote
            #     olericultura.save()
            #
            # fruticulturas = fruticulturas_forms.save(commit=False)
            # for fruticultura in fruticulturas:
            #     fruticultura.lote = lote
            #     fruticultura.save()
            #
            # atividades_extrativistas = atividades_extrativistas_forms.save(commit=False)
            # for atividade_extrativista in atividades_extrativistas:
            #     atividade_extrativista.lote = lote
            #     atividade_extrativista.save()
            #
            # producoes_florestais = producoes_florestais_forms.save(commit=False)
            # for producao_florestal in producoes_florestais:
            #     producao_florestal.lote = lote
            #     producao_florestal.save()
            #
            # bovinoculturas = bovinoculturas_forms.save(commit=False)
            # for bovinocultura in bovinoculturas:
            #     bovinocultura.lote = lote
            #     bovinocultura.save()
            #
            # outras_criacoes = outras_criacoes_forms.save(commit=False)
            # for outra_criacao in outras_criacoes:
            #     outra_criacao.lote = lote
            #     outra_criacao.save()
            #
            # bovinoculturas_leiteira = bovinoculturas_leiteira_forms.save(commit=False)
            # for bovinocultura_leiteira in bovinoculturas_leiteira:
            #     bovinocultura_leiteira.lote = lote
            #     bovinocultura_leiteira.save()
            #
            # bovinoculturas_corte = bovinoculturas_corte_forms.save(commit=False)
            # for bovinocultura_corte in bovinoculturas_corte:
            #     bovinocultura_corte.lote = lote
            #     bovinocultura_corte.save()
            #
            # origens_animais = origens_animais_forms.save(commit=False)
            # for origem_animal in origens_animais:
            #     origem_animal.lote = lote
            #     origem_animal.save()
            #
            # niveis_tecnologicos_producao_animal = niveis_tecnologicos_producao_animal_forms.save(commit=False)
            #
            # for nivel_tecnologico_producao_animal in niveis_tecnologicos_producao_animal:
            #     nivel_tecnologico_producao_animal.lote = lote
            #     nivel_tecnologico_producao_animal.save()
            #     lote.possui_capineira = models.Lote.CHOICE_SIM
            #     lote.save()
            #
            # processados_beneficiados = processados_beneficiados_forms.save(commit=False)
            # for processado_beneficiado in processados_beneficiados:
            #     processado_beneficiado.lote = lote
            #     processado_beneficiado.save()

            template = reverse('core:listar_diagnosticos_por_projeto_assentamento',
                               kwargs={'contrato_id': projeto_assentamento.contrato_id,
                                       'pa_id': projeto_assentamento.pk})
            return redirect(template)
    template_name = 'core/editar_diagnostico.html'
    context = {
        'form': form,
        'projeto_assentamento': projeto_assentamento,
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

    if request.method == "POST":
        form = forms.DiagnosticoForm(
            request.POST,
            instance=diagnostico,
            initial={
                'projeto_assentamento': projeto_assentamento.pk
            }
        )

        contatos_forms = forms.ContatoInlineFormSet(
            request.POST,
            prefix='contatos',
            queryset=form.instance.contatos.all()
        )
        documentos_lote_forms = forms.DocumentoLoteInlineFormSet(
            request.POST,
            prefix='documentos_lote',
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
        fontes_agua_forms = forms.FonteAguaInlineFormSet(
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
        culturas_forms = forms.CulturaInlineFormSet(
            request.POST,
            prefix='culturas',
            queryset=form.instance.producoesVegetais.filter(classificacao=models.Cultura.CLASSIFICACAO_CULTURA)
        )
        olericulturas_forms = forms.OlericulturaInlineFormSet(
            request.POST,
            prefix='olericulturas',
            queryset=form.instance.producoesVegetais.filter(classificacao=models.Cultura.CLASSIFICACAO_OLERICULTURA)
        )
        fruticulturas_forms = forms.FruticulturaInlineFormSet(
            request.POST,
            prefix='fruticulturas',
            queryset=form.instance.producoesVegetais.filter(classificacao=models.Cultura.CLASSIFICACAO_FRUTICULTURA)
        )
        atividades_extrativistas_forms = forms.AtividadeExtrativistaInlineFormSet(
            request.POST,
            prefix='atividades_extrativistas',
            queryset=form.instance.atividadesExtrativistas.all()
        )
        producoes_florestais_forms = forms.ProducaoFlorestalInlineFormSet(
            request.POST,
            prefix='producoes_florestais',
            queryset=form.instance.producoesFlorestais.all()
        )
        bovinoculturas_forms = forms.BovinoculturaInlineFormSet(
            request.POST,
            prefix='bovinoculturas',
            queryset=form.instance.producoesAnimais.filter(
                classificacao=models.Bovinocultura.CLASSIFICACAO_BOVINOCULTURA)
        )
        outras_criacoes_forms = forms.OutraCriacaoInlineFormSet(
            request.POST,
            prefix='outras_criacoes',
            queryset=form.instance.producoesAnimais.filter(
                classificacao=models.Bovinocultura.CLASSIFICACAO_OUTRA_CRIACAO)
        )
        bovinoculturas_leiteira_forms = forms.BovinoculturaLeiteiraInlineFormSet(
            request.POST,
            prefix='bovinoculturas_leiteira',
            queryset=form.instance.descartesAnimais.filter(
                tipo_criacao=models.BovinoculturaLeiteira.TIPO_CRIACAO_GADO_LEITEIRO)
        )
        bovinoculturas_corte_forms = forms.BovinoculturaCorteInlineFormSet(
            request.POST,
            prefix='bovinoculturas_corte',
            queryset=form.instance.descartesAnimais.filter(
                tipo_criacao=models.BovinoculturaCorte.TIPO_CRIACAO_GADO_DE_CORTE)
        )
        origens_animais_forms = forms.OrigemAnimalInlineFormSet(
            request.POST,
            prefix='origens_animais',
            queryset=form.instance.produtosOrigemAnimal.filter(
                classificacao=models.OrigemAnimal.CLASSIFICACAO_ORIGEM_ANIMAL)
        )
        niveis_tecnologicos_producao_animal_forms = forms.NivelTecnologicoProducaoAnimalInlineFormSet(
            request.POST,
            prefix='niveis_tecnologicos_producao_animal',
            queryset=form.instance.niveisTecnologicosProducaoAnimal.all()
        )
        processados_beneficiados_forms = forms.ProcessadoBeneficiadoInlineFormSet(
            request.POST,
            prefix='processados_beneficiados',
            queryset=form.instance.produtosOrigemAnimal.filter(
                classificacao=models.ProcessadoBeneficiado.CLASSIFICACAO_PROCESSADO_BENEFICIADO)
        )

        if form.is_valid() and contatos_forms.is_valid() and documentos_lote_forms.is_valid() and beneficios_forms.is_valid() \
            and auto_declaracoes_forms.is_valid() and estruturas_organizativas_forms.is_valid() \
            and fontes_agua_forms.is_valid() and tratamentos_agua_forms.is_valid() and construcoes_lote_forms.is_valid() \
            and bens_produtivos_forms.is_valid() and aplicacoes_creditos_forms.is_valid() \
            and creditos_bancarios_forms.is_valid() and culturas_forms.is_valid() and olericulturas_forms.is_valid() \
            and fruticulturas_forms.is_valid() and atividades_extrativistas_forms.is_valid() \
            and producoes_florestais_forms.is_valid() and bovinoculturas_forms.is_valid() and outras_criacoes_forms.is_valid() \
            and bovinoculturas_leiteira_forms.is_valid() and bovinoculturas_corte_forms.is_valid() \
            and origens_animais_forms.is_valid() and niveis_tecnologicos_producao_animal_forms.is_valid() \
            and processados_beneficiados_forms.is_valid():
            lote = form.save(commit=False)
            lote.save()

            contatos = contatos_forms.save(commit=False)
            for contato in contatos:
                contato.lote = lote
                contato.save()

            for contato in contatos_forms.deleted_objects:
                contato.delete()

            documentos_lote = documentos_lote_forms.save(commit=False)
            for documento in documentos_lote:
                documento.lote = lote
                documento.save()

            for documento in documentos_lote_forms.deleted_objects:
                documento.delete()

            beneficios = beneficios_forms.save(commit=False)
            for beneficio in beneficios:
                beneficio.lote = lote
                beneficio.save()

            for beneficio in beneficios_forms.deleted_objects:
                beneficio.delete()

            auto_declaracoes = auto_declaracoes_forms.save(commit=False)
            for auto_declaracao in auto_declaracoes:
                auto_declaracao.lote = lote
                auto_declaracao.save()

            for auto_declaracao in auto_declaracoes_forms.deleted_objects:
                auto_declaracao.delete()

            estruturas_organizativas = estruturas_organizativas_forms.save(commit=False)
            for estrutura_organizativa in estruturas_organizativas:
                estrutura_organizativa.lote = lote
                estrutura_organizativa.save()

            for estrutura_organizativa in estruturas_organizativas_forms.deleted_objects:
                estrutura_organizativa.delete()

            fontes_agua = fontes_agua_forms.save(commit=False)
            for fonte_agua in fontes_agua:
                fonte_agua.lote = lote
                fonte_agua.save()

            for fonte_agua in fontes_agua_forms.deleted_objects:
                fonte_agua.delete()

            tratamentos_agua = tratamentos_agua_forms.save(commit=False)
            for tratamento_agua in tratamentos_agua:
                tratamento_agua.lote = lote
                tratamento_agua.save()

            for tratamento_agua in tratamentos_agua_forms.deleted_objects:
                tratamento_agua.delete()

            construcoes_lote = construcoes_lote_forms.save(commit=False)
            for construcao_lote in construcoes_lote:
                construcao_lote.lote = lote
                construcao_lote.save()

            for construcao_lote in construcoes_lote_forms.deleted_objects:
                construcao_lote.delete()

            bens_produtivos = bens_produtivos_forms.save(commit=False)
            for bem_produtivo in bens_produtivos:
                bem_produtivo.lote = lote
                bem_produtivo.save()

            for bem_produtivo in bens_produtivos_forms.deleted_objects:
                bem_produtivo.delete()

            aplicacoes_creditos = aplicacoes_creditos_forms.save(commit=False)
            for aplicacao_credito in aplicacoes_creditos:
                aplicacao_credito.lote = lote
                aplicacao_credito.save()

            for aplicacao_credito in aplicacoes_creditos_forms.deleted_objects:
                aplicacao_credito.delete()

            creditos_bancarios = creditos_bancarios_forms.save(commit=False)
            for credito_bancario in creditos_bancarios:
                credito_bancario.lote = lote
                credito_bancario.save()

            for credito_bancario in creditos_bancarios_forms.deleted_objects:
                credito_bancario.delete()

            culturas = culturas_forms.save(commit=False)
            for cultura in culturas:
                cultura.classificacao = models.Cultura.CLASSIFICACAO_CULTURA
                cultura.lote = lote
                cultura.save()

            for cultura in culturas_forms.deleted_objects:
                cultura.delete()

            olericulturas = olericulturas_forms.save(commit=False)
            for olericultura in olericulturas:
                olericultura.lote = lote
                olericultura.save()

            for olericultura in olericulturas_forms.deleted_objects:
                olericultura.delete()

            fruticulturas = fruticulturas_forms.save(commit=False)
            for fruticultura in fruticulturas:
                fruticultura.lote = lote
                fruticultura.save()

            for fruticultura in fruticulturas_forms.deleted_objects:
                fruticultura.delete()

            atividades_extrativistas = atividades_extrativistas_forms.save(commit=False)
            for atividade_extrativista in atividades_extrativistas:
                atividade_extrativista.lote = lote
                atividade_extrativista.save()

            for atividade_extrativista in atividades_extrativistas_forms.deleted_objects:
                atividade_extrativista.delete()

            producoes_florestais = producoes_florestais_forms.save(commit=False)
            for producao_florestal in producoes_florestais:
                producao_florestal.lote = lote
                producao_florestal.save()

            for producao_florestal in producoes_florestais_forms.deleted_objects:
                producao_florestal.delete()

            bovinoculturas = bovinoculturas_forms.save(commit=False)
            for bovinocultura in bovinoculturas:
                bovinocultura.lote = lote
                bovinocultura.save()

            for bovinocultura in bovinoculturas_forms.deleted_objects:
                bovinocultura.delete()

            outras_criacoes = outras_criacoes_forms.save(commit=False)
            for outra_criacao in outras_criacoes:
                outra_criacao.lote = lote
                outra_criacao.save()

            for outra_criacao in outras_criacoes_forms.deleted_objects:
                outra_criacao.delete()

            bovinoculturas_leiteira = bovinoculturas_leiteira_forms.save(commit=False)
            for bovinocultura_leiteira in bovinoculturas_leiteira:
                bovinocultura_leiteira.lote = lote
                bovinocultura_leiteira.save()

            for bovinocultura_leiteira in bovinoculturas_leiteira_forms.deleted_objects:
                bovinocultura_leiteira.delete()

            bovinoculturas_corte = bovinoculturas_corte_forms.save(commit=False)
            for bovinocultura_corte in bovinoculturas_corte:
                bovinocultura_corte.lote = lote
                bovinocultura_corte.save()

            for bovinocultura_corte in bovinoculturas_corte_forms.deleted_objects:
                bovinocultura_corte.delete()

            origens_animais = origens_animais_forms.save(commit=False)
            for origem_animal in origens_animais:
                origem_animal.lote = lote
                origem_animal.save()

            for origem_animal in origens_animais_forms.deleted_objects:
                origem_animal.delete()

            niveis_tecnologicos_producao_animal = niveis_tecnologicos_producao_animal_forms.save(commit=False)
            for nivel_tecnologico_producao_animal in niveis_tecnologicos_producao_animal:
                nivel_tecnologico_producao_animal.lote = lote
                nivel_tecnologico_producao_animal.save()

            for nivel_tecnologico_producao_animal in niveis_tecnologicos_producao_animal_forms.deleted_objects:
                nivel_tecnologico_producao_animal.delete()

            processados_beneficiados = processados_beneficiados_forms.save(commit=False)
            for processado_beneficiado in processados_beneficiados:
                processado_beneficiado.lote = lote
                processado_beneficiado.save()

            for processado_beneficiado in processados_beneficiados_forms.deleted_objects:
                processado_beneficiado.delete()

            template = reverse('core:listar_diagnosticos_por_projeto_assentamento',
                               kwargs={'contrato_id': projeto_assentamento.contrato_id,
                                       'pa_id': projeto_assentamento.pk})
            return redirect(template)
    template_name = 'core/editar_diagnostico.html'
    context = {
        'form': form,
        'projeto_assentamento': projeto_assentamento,
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
