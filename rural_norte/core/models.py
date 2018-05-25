from django.conf import settings
from django.db import models
from cuser.fields import CurrentUserField
from model_utils import Choices


class AuditoriaAbstractModel(models.Model):
    cadastrado_por = CurrentUserField(
        add_only=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_cadastrado_por'
    )

    cadastrado_em = models.DateTimeField(
        auto_now_add=True,
        null=True
    )

    modificado_por = CurrentUserField(
        null=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_modificado_por'
    )

    modificado_em = models.DateTimeField(
        auto_now=True,
        null=True
    )

    desativado_por = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_desativado_por',
        blank=True
    )

    desativado_em = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

    def _ativo(self):
        if self.desativado_em:
            return False
        else:
            return True

    _ativo.boolean = True
    ativo = property(_ativo)


class ProjetoAssentamento(AuditoriaAbstractModel):
    CONTRATO_10 = 10
    CONTRATO_11 = 11
    CONTRATO_18 = 18

    contrato_choices = Choices(
        (CONTRATO_10, '10.000/2015'),
        (CONTRATO_11, '11.000/2015'),
        (CONTRATO_18, '18.000/2015')
    )
    contrato = models.IntegerField('Contrato', choices=contrato_choices)
    codigo = models.CharField('Código do PA', max_length=15)
    nome = models.CharField('Nome do PA', max_length=50)
    municipio = models.CharField('Município', max_length=100)
    data_criacao = models.DateField('Data de Criação')
    capacidade_projeto = models.IntegerField('Capacidade do Projeto')

    def __str__(self):
        return '%s | %s' % (self.codigo, self.nome)

    class Meta:
        verbose_name = 'Projeto de Assentamento'
        verbose_name_plural = 'Projetos de Assentamento'
        ordering = ['codigo']


class Lote(AuditoriaAbstractModel):
    projeto_assentamento = models.ForeignKey(
        ProjetoAssentamento, verbose_name='PA', related_name='lotes', on_delete=models.CASCADE
    )
    data_homologacao = models.DateField('Data Homologação', blank=True, null=True)
    codigo_sipra = models.CharField('Código SIPRA', max_length=15, blank=True, null=True)
    area = models.DecimalField('Área (ha)', max_digits=10, decimal_places=4)
    numero = models.IntegerField('Lote N.º')
    entrevistador = models.CharField('Nome do Entrevistador', max_length=50)
    coordenada_x = models.CharField('Coordenada "X"', max_length=30)
    coordenada_y = models.CharField('Coordenada "Y"', max_length=30)

    CHOICE_SIM = 1
    CHOICE_NAO = 0

    sim_nao_choices = Choices(
        (CHOICE_SIM, 'Sim'),
        (CHOICE_NAO, 'Não')
    )
    outra_familia_no_lote = models.IntegerField(
        'Existe outra família que mora na parcela/lote?',
        choices=sim_nao_choices
    )
    cad_unico = models.IntegerField('CAD - Único', choices=sim_nao_choices)
    ocupante_irregular = models.IntegerField('Ocupante irregular?', choices=sim_nao_choices)
    ocupante_irregular_tempo = models.CharField(
        'Em caso afirmativo, há quanto tempo?', max_length=30, blank=True, null=True
    )
    recebe_beneficio_social = models.IntegerField(
        '3. Algum dos membros da família recebe algum tipo de Benefício Social?',
        choices=sim_nao_choices
    )
    moradia_assentamento = models.IntegerField('7. Possui moradia no assentamento?', choices=sim_nao_choices)

    TIPO_PAREDE_ALVENARIA = 10
    TIPO_PAREDE_TABUAS_MADEIRA = 20
    TIPO_PAREDE_TAPUMES_OU_CHAPAS_MADEIRA = 30
    TIPO_PAREDE_FOLHAS_DE_ZINCO = 40
    TIPO_PAREDE_BARRO_OU_ADOBE = 50
    TIPO_PAREDE_LONA = 60
    TIPO_PAREDE_OUTROS = 70

    tipo_parede_externa_choices = Choices(
        (TIPO_PAREDE_ALVENARIA, 'Alvenaria'),
        (TIPO_PAREDE_TABUAS_MADEIRA, 'Tábuas / Madeira'),
        (TIPO_PAREDE_TAPUMES_OU_CHAPAS_MADEIRA, 'Tapumes ou chapas de madeira'),
        (TIPO_PAREDE_FOLHAS_DE_ZINCO, 'Folha de zinco'),
        (TIPO_PAREDE_BARRO_OU_ADOBE, 'Barro ou adobe'),
        (TIPO_PAREDE_LONA, 'Lona'),
        (TIPO_PAREDE_OUTROS, 'Outros')
    )
    tipo_parede_externa = models.IntegerField(
        '8. Qual tipo de parede externa predominante da moradia?', choices=tipo_parede_externa_choices,
        blank=True, null=True
    )

    TIPO_INSTALACAO_ELETRICA_NAO_INSTALADA = 10
    TIPO_INSTALACAO_ELETRICA_INSTALADA_APENAS_PARA_MORADIA = 20
    TIPO_INSTALACAO_ELETRICA_INSTALADA_PARA_MORADIA_E_OUTROS_USOS = 30
    TIPO_INSTALACAO_ELETRICA_OUTROS = 40

    tipo_instalacao_eletrica_choices = Choices(
        (TIPO_INSTALACAO_ELETRICA_NAO_INSTALADA, 'Não instalada'),
        (TIPO_INSTALACAO_ELETRICA_INSTALADA_APENAS_PARA_MORADIA, 'Instalada apenas para moradia'),
        (TIPO_INSTALACAO_ELETRICA_INSTALADA_PARA_MORADIA_E_OUTROS_USOS, 'Instalada para moradia e outros usos'),
        (TIPO_INSTALACAO_ELETRICA_OUTROS, 'Outros')
    )
    tipo_instalacao_eletrica = models.IntegerField(
        '9. Instalação de energia elétrica?', choices=tipo_instalacao_eletrica_choices,
        blank=True, null=True
    )

    TIPO_INSTALACAO_SANITARIA_BANHEIRO_COM_FOSSA_SEPTICA = 10
    TIPO_INSTALACAO_SANITARIA_BANHEIRO_COM_FOSSA_NEGRA = 20
    TIPO_INSTALACAO_SANITARIA_PRIVADA_LATRINA = 30
    TIPO_INSTALACAO_SANITARIA_NENHUMA = 40

    tipo_instalacao_sanitaria_choices = Choices(
        (TIPO_INSTALACAO_SANITARIA_BANHEIRO_COM_FOSSA_SEPTICA, 'Banheiro com fossa séptica'),
        (TIPO_INSTALACAO_SANITARIA_BANHEIRO_COM_FOSSA_NEGRA, 'Banheiro com fossa negra'),
        (TIPO_INSTALACAO_SANITARIA_PRIVADA_LATRINA, 'Privada / latrina'),
        (TIPO_INSTALACAO_SANITARIA_NENHUMA, 'Nenhuma')
    )
    tipo_instalacao_sanitaria = models.IntegerField(
        '10. Qual é o tipo de instalação sanitária?', choices=tipo_instalacao_sanitaria_choices,
        blank=True, null=True
    )

    LOCALIZACAO_FONTE_DE_AGUA_DENTRO_DO_SEU_LOTE = 1
    LOCALIZACAO_FONTE_DE_AGUA_FORA_DO_SEU_LOTE = 2

    localizacao_fonte_agua_choices = Choices(
        (LOCALIZACAO_FONTE_DE_AGUA_DENTRO_DO_SEU_LOTE, 'Dentro do seu lote'),
        (LOCALIZACAO_FONTE_DE_AGUA_FORA_DO_SEU_LOTE, 'Fora do seu lote')
    )
    localizacao_fonte_agua = models.IntegerField(
        '13. Onde está localizada a fonte de água que abastece sua residência?', choices=localizacao_fonte_agua_choices
    )
    abastecimento_agua_suficiente = models.IntegerField(
        '14. A água que abastece a residência é suficiente?', choices=sim_nao_choices
    )

    QUANTAS_FAMILIAS_UTILIZAM_MESMA_FONTE_DE_AGUA_NENHUMA = 10
    QUANTAS_FAMILIAS_UTILIZAM_MESMA_FONTE_DE_AGUA_UMA_OUTRA_FAMILIA_ALEM_DA_SUA = 20
    QUANTAS_FAMILIAS_UTILIZAM_MESMA_FONTE_DE_AGUA_MAIS_DE_UMA = 30

    quantas_familias_utilizam_mesma_fonte_agua_choices = Choices(
        (QUANTAS_FAMILIAS_UTILIZAM_MESMA_FONTE_DE_AGUA_NENHUMA, 'Nenhuma'),
        (QUANTAS_FAMILIAS_UTILIZAM_MESMA_FONTE_DE_AGUA_UMA_OUTRA_FAMILIA_ALEM_DA_SUA,
         'Uma outra família, além da sua família'),
        (QUANTAS_FAMILIAS_UTILIZAM_MESMA_FONTE_DE_AGUA_MAIS_DE_UMA, 'Mais de uma')
    )
    quantas_familias_utilizam_mesma_fonte_agua = models.IntegerField(
        '15. Quantas famílias (além da sua) fazem o uso da mesma fonte de água que abastece o seu lote?',
        choices=quantas_familias_utilizam_mesma_fonte_agua_choices
    )
    quantidade_familias_utilizacao_mesma_fonte_agua = models.IntegerField('Mais de uma. Quantas?', blank=True,
                                                                          null=True)

    AGUA_PARA_ANIMAIS_PLANTIO_SIM_OS_ANIMAIS_VAO_ATE_CURSO_DAGUA_OU_REPRESA = 10
    AGUA_PARA_ANIMAIS_PLANTIO_SIM_AGUA_PUXADA_DE_CURSO_DAGUA_OU_REPRESA = 20
    AGUA_PARA_ANIMAIS_PLANTIO_SIM_TEMOS_POCO_EXCLUSIVO_PARA_ANIMAIS = 30
    AGUA_PARA_ANIMAIS_PLANTIO_SIM_MESMA_AGUA_QUE_VEM_PARA_CASA = 40
    AGUA_PARA_ANIMAIS_PLANTIO_NAO_HA_AGUA_PARA_ANIMAIS = 50
    AGUA_PARA_ANIMAIS_PLANTIO_SIM_EXISTE_AGUA_PARA_PLANTIO_IRRIGADO = 60
    AGUA_PARA_ANIMAIS_PLANTIO_NAO_EXISTE_AGUA_PARA_PLANTIO_IRRIGADO = 70
    AGUA_PARA_ANIMAIS_PLANTIO_OUTROS = 80

    agua_para_animais_plantio_choices = Choices(
        (AGUA_PARA_ANIMAIS_PLANTIO_SIM_OS_ANIMAIS_VAO_ATE_CURSO_DAGUA_OU_REPRESA,
         "Sim, os animais vão até um curso d'água ou represa"),
        (AGUA_PARA_ANIMAIS_PLANTIO_SIM_AGUA_PUXADA_DE_CURSO_DAGUA_OU_REPRESA,
         "Sim, a água é puxada de um curso d'água ou represa"),
        (AGUA_PARA_ANIMAIS_PLANTIO_SIM_TEMOS_POCO_EXCLUSIVO_PARA_ANIMAIS,
         'Sim, temos um poço exclusivo para os animais'),
        (AGUA_PARA_ANIMAIS_PLANTIO_SIM_MESMA_AGUA_QUE_VEM_PARA_CASA, 'Sim, é a mesma água que vem para a casa'),
        (AGUA_PARA_ANIMAIS_PLANTIO_NAO_HA_AGUA_PARA_ANIMAIS, 'Não há água para animais'),
        (AGUA_PARA_ANIMAIS_PLANTIO_SIM_EXISTE_AGUA_PARA_PLANTIO_IRRIGADO,
         'Sim, existe água para plantio(s) irrigado(s)'),
        (
            AGUA_PARA_ANIMAIS_PLANTIO_NAO_EXISTE_AGUA_PARA_PLANTIO_IRRIGADO,
            'Não existe água para plantio(s) irrigado(s)'),
        (AGUA_PARA_ANIMAIS_PLANTIO_OUTROS, 'Outros')
    )
    agua_para_animais_plantio = models.IntegerField(
        '16. No lote tem água para os animais / Plantio?', choices=agua_para_animais_plantio_choices
    )
    agua_para_animais_plantio_outros = models.CharField(
        'Água para animais/plantio (Outros)', max_length=50, blank=True, null=True
    )

    REGULARIDADE_ABASTECIMENTO_AGUA_SEMPRE_TEM_AGUA = 10
    REGULARIDADE_ABASTECIMENTO_AGUA_FALTA_AGUA_AS_VEZES = 20
    REGULARIDADE_ABASTECIMENTO_AGUA_FALTA_AGUA_COM_FREQUENCIA = 30
    REGULARIDADE_ABASTECIMENTO_AGUA_NUNCA_TEM_AGUA = 40

    regularidade_abastecimento_agua_choices = Choices(
        (REGULARIDADE_ABASTECIMENTO_AGUA_SEMPRE_TEM_AGUA, 'Sempre tem água'),
        (REGULARIDADE_ABASTECIMENTO_AGUA_FALTA_AGUA_AS_VEZES, 'Falta água às vezes'),
        (REGULARIDADE_ABASTECIMENTO_AGUA_FALTA_AGUA_COM_FREQUENCIA, 'Falta água com frequência'),
        (REGULARIDADE_ABASTECIMENTO_AGUA_NUNCA_TEM_AGUA, 'Nunca tem água')
    )
    regularidade_abastecimento_agua = models.IntegerField(
        '17. Regularidade de abastecimento de água',
        choices=regularidade_abastecimento_agua_choices
    )

    TIPO_ESTRADA_DE_ACESSO_ASFALTO = 10
    TIPO_ESTRADA_DE_ACESSO_ESTRADA_CASCALHADA = 20
    TIPO_ESTRADA_DE_ACESSO_ESTRADA_DE_TERRA = 30
    TIPO_ESTRADA_DE_ACESSO_TRILHEIRO = 40
    TIPO_ESTRADA_DE_ACESSO_INEXISTENTE = 50

    tipo_estrada_acesso_choices = Choices(
        (TIPO_ESTRADA_DE_ACESSO_ASFALTO, 'Asfalto'),
        (TIPO_ESTRADA_DE_ACESSO_ESTRADA_CASCALHADA, 'Estrada cascalhada'),
        (TIPO_ESTRADA_DE_ACESSO_ESTRADA_DE_TERRA, 'Estrada de terra'),
        (TIPO_ESTRADA_DE_ACESSO_TRILHEIRO, 'Trilheiro'),
        (TIPO_ESTRADA_DE_ACESSO_INEXISTENTE, 'Inexistente')
    )
    tipo_estrada_acesso = models.IntegerField(
        '18. Como é o acesso ao lote?',
        choices=tipo_estrada_acesso_choices
    )

    SITUACAO_ESTRADA_ACESSO_BOA = 10
    SITUACAO_ESTRADA_ACESSO_RAZOAVEL = 20
    SITUACAO_ESTRADA_ACESSO_RUIM = 30
    SITUACAO_ESTRADA_ACESSO_PESSIMA = 40

    situacao_estrada_acesso_choices = Choices(
        (SITUACAO_ESTRADA_ACESSO_BOA, 'Boa'),
        (SITUACAO_ESTRADA_ACESSO_RAZOAVEL, 'Razoável'),
        (SITUACAO_ESTRADA_ACESSO_RUIM, 'Ruim'),
        (SITUACAO_ESTRADA_ACESSO_PESSIMA, 'Péssima')
    )
    situacao_estrada_acesso = models.IntegerField(
        '19. Situação anual da estrada principal acesso ao lote?',
        choices=situacao_estrada_acesso_choices
    )

    SITUACAO_CERCADO_LOTE_TOTALMENTE_CERCADO_COM_DIVISOES_INTERNAS = 10
    SITUACAO_CERCADO_LOTE_TOTALMENTE_CERCADO_SEM_DIVISOES_INTERNAS = 20
    SITUACAO_CERCADO_LOTE_PARCIALMENTE_CERCADO = 30
    SITUACAO_CERCADO_LOTE_NAO_ESTA_CERCADO = 40

    situacao_cercado_lote_choices = Choices(
        (SITUACAO_CERCADO_LOTE_TOTALMENTE_CERCADO_COM_DIVISOES_INTERNAS, 'Totalmente cercado, com divisões internas'),
        (SITUACAO_CERCADO_LOTE_TOTALMENTE_CERCADO_SEM_DIVISOES_INTERNAS, 'Totalmente cercado, sem divisões internas'),
        (SITUACAO_CERCADO_LOTE_PARCIALMENTE_CERCADO, 'Parcialmente cercado'),
        (SITUACAO_CERCADO_LOTE_NAO_ESTA_CERCADO, 'Não está cercado')
    )
    situacao_cercado_lote = models.IntegerField(
        '20. Como está cercado o lote?',
        choices=situacao_cercado_lote_choices
    )
    area_preservacao_permanente = models.IntegerField(
        '38. Existe Área de Preservação Permanente (APP) dentro do seu lote/parcela?', choices=sim_nao_choices
    )
    area_preservacao_permanente_cercada = models.IntegerField(
        '39. A Área de Preservação Permanente está cercada ou isolada?', choices=sim_nao_choices
    )
    possui_capineira = models.IntegerField(
        'Possui Capineira?', choices=sim_nao_choices, default=CHOICE_NAO
    )
    possui_pastagem_em_pastejo_rotacionado = models.IntegerField(
        '34. Possui Pastagem em Pastejo Rotacionado?', choices=sim_nao_choices
    )
    area_pastejo_rotacionado = models.DecimalField(
        'Tamanho da área em sistema de Pastejo Rotacionado (ha)', max_digits=10, decimal_places=4, blank=True, null=True
    )
    pratica_inseminacao_artificial_no_rebanho_leiteiro = models.IntegerField(
        '35. Pratica inseminação aritificial no rebanho leiteiro?', choices=sim_nao_choices
    )
    necessita_licenciamento_ambiental = models.IntegerField(
        'Necessita de licenciamento ambiental de atividade?', choices=sim_nao_choices, default=CHOICE_NAO
    )
    necessita_autoriacao_exploracao_florestal_queima_controlada = models.IntegerField(
        '45. Necessita de autorização de exploração florestal e/ou queima controlada?', choices=sim_nao_choices
    )

    QUALIDADE_SERVICO_SAUDE_OTIMO = 10
    QUALIDADE_SERVICO_SAUDE_BOM = 20
    QUALIDADE_SERVICO_SAUDE_RUIM = 30
    QUALIDADE_SERVICO_SAUDE_PESSIMO = 40

    qualidade_servico_saude_choices = Choices(
        (QUALIDADE_SERVICO_SAUDE_OTIMO, 'Ótimo'),
        (QUALIDADE_SERVICO_SAUDE_BOM, 'Bom'),
        (QUALIDADE_SERVICO_SAUDE_RUIM, 'Ruim'),
        (QUALIDADE_SERVICO_SAUDE_PESSIMO, 'Péssimo')
    )
    qualidade_servico_saude = models.IntegerField(
        '48. Como os moradores consideram o serviço de saúde no assentamento?', choices=qualidade_servico_saude_choices
    )

    FREQUENCIA_ATIVIDADE_FISICA_DIARIAMENTE = 10
    FREQUENCIA_ATIVIDADE_FISICA_DUAS_VEZES_POR_SEMANA = 20
    FREQUENCIA_ATIVIDADE_FISICA_MAIS_DE_DUAS_VEZES_POR_SEMANA = 30
    FREQUENCIA_ATIVIDADE_FISICA_NAO_PRATICA = 40

    frequencia_atividade_fisica_choices = Choices(
        (FREQUENCIA_ATIVIDADE_FISICA_DIARIAMENTE, 'Diariamente'),
        (FREQUENCIA_ATIVIDADE_FISICA_DUAS_VEZES_POR_SEMANA, 'Duas vezes por semana'),
        (FREQUENCIA_ATIVIDADE_FISICA_MAIS_DE_DUAS_VEZES_POR_SEMANA, 'Mais de duas vezes por semana'),
        (FREQUENCIA_ATIVIDADE_FISICA_NAO_PRATICA, 'Não pratica')
    )
    frequencia_atividade_fisica = models.IntegerField(
        '51. Com que frequência praticam atividades físicas ou esportes?', choices=frequencia_atividade_fisica_choices
    )
    OFERTA_TRANSPORTE_INTERNO_SIM = 1
    OFERTA_TRANSPORTE_INTERNO_NAO = 0
    OFERTA_TRANSPORTE_INTERNO_NAO_SE_APLICA = 99

    oferta_transporte_interno_choices = Choices(
        (OFERTA_TRANSPORTE_INTERNO_SIM, 'Sim'),
        (OFERTA_TRANSPORTE_INTERNO_NAO, 'Não'),
        (OFERTA_TRANSPORTE_INTERNO_NAO_SE_APLICA, 'Não se aplica')
    )
    oferta_transporte_interno = models.IntegerField(
        '54. Para a escola do assentamento há oferta de transporte interno?', choices=oferta_transporte_interno_choices
    )

    def __str__(self):
        return '%s - %s' % (self.projeto_assentamento.nome, self.codigo_sipra)

    class Meta:
        verbose_name = 'Campo Diagnóstico'
        verbose_name_plural = 'Campo Diagnósticos'


class DocumentoLote(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='documentos', on_delete=models.CASCADE)

    TIPO_DOCUMENTO_CONTRATO_DE_ASSENTAMENTO = 10
    TIPO_DOCUMENTO_CONTRATO_DE_CONCESSAO_DE_USO = 20
    TIPO_DOCUMENTO_TITULO_DEFINITIVO_NAO_REGISTRADO = 30
    TIPO_DOCUMENTO_TITULO_DEFINITIVO_REGISTRADO_CARTORIO = 40
    TIPO_DOCUMENTO_MATRICULA_DA_PROPRIEDADE = 50

    tipo_documento_choices = Choices(
        (TIPO_DOCUMENTO_CONTRATO_DE_ASSENTAMENTO, 'Contrato de Assentamento'),
        (TIPO_DOCUMENTO_CONTRATO_DE_CONCESSAO_DE_USO, 'Contrato de Concessão de Uso - CCU'),
        (TIPO_DOCUMENTO_TITULO_DEFINITIVO_NAO_REGISTRADO, 'Título Definitivo - não registrado'),
        (TIPO_DOCUMENTO_TITULO_DEFINITIVO_REGISTRADO_CARTORIO, 'Título Definitivo - registrado cartório'),
        (TIPO_DOCUMENTO_MATRICULA_DA_PROPRIEDADE, 'Matrícula da Propriedade')
    )
    tipo_documento = models.IntegerField('Documento', choices=tipo_documento_choices)

    def __str__(self):
        return self.tipo_documento_choices[self.tipo_documento]

    class Meta:
        verbose_name = ''
        verbose_name_plural = '1. Quais documentos o lote possui?'


class BeneficioSocial(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='beneficios', on_delete=models.CASCADE)

    TIPO_BENEFICIO_APOSENTADORIA_POR_TEMPO_DE_SERVICO_IDADE = 10
    TIPO_BENEFICIO_APOSENTADORIA_POR_INVALIDEZ = 20
    TIPO_BENEFICIO_AUXILIO_MATERNIDADE = 30
    TIPO_BENEFICIO_BOLSA_FAMILIA = 40
    TIPO_BENEFICIO_BOLSA_VERDE = 50
    TIPO_BENEFICIO_OUTROS = 60

    tipo_beneficio_choices = Choices(
        (TIPO_BENEFICIO_APOSENTADORIA_POR_TEMPO_DE_SERVICO_IDADE, 'Aposentadoria por tempo de serviço/idade'),
        (TIPO_BENEFICIO_APOSENTADORIA_POR_INVALIDEZ, 'Aposentadoria por invalidez'),
        (TIPO_BENEFICIO_AUXILIO_MATERNIDADE, 'Auxílio maternidade'),
        (TIPO_BENEFICIO_BOLSA_FAMILIA, 'Bolsa família'),
        (TIPO_BENEFICIO_BOLSA_VERDE, 'Bolsa verde'),
        (TIPO_BENEFICIO_OUTROS, 'Outros')
    )
    tipo_beneficio = models.IntegerField('Benefício', choices=tipo_beneficio_choices)
    outros = models.CharField('Outros', max_length=30, blank=True, null=True)

    def __str__(self):
        return self.tipo_beneficio_choices[self.tipo_beneficio]

    class Meta:
        verbose_name = ''
        verbose_name_plural = '4. Quais os tipos de benefício?'


class AutoDeclaracaoEtnia(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='autoDeclaracoes', on_delete=models.CASCADE)

    TIPO_DECLARACAO_ETNIA_NEGROS = 10
    TIPO_DECLARACAO_ETNIA_PARDOS = 20
    TIPO_DECLARACAO_ETNIA_BRANCOS = 30
    TIPO_DECLARACAO_ETNIA_INDIOS = 40
    TIPO_DECLARACAO_ETNIA_ORIENTAIS = 50
    TIPO_DECLARACAO_ETNIA_OUTROS = 60

    tipo_declaracao_etnia_choices = Choices(
        (TIPO_DECLARACAO_ETNIA_NEGROS, 'Negros'),
        (TIPO_DECLARACAO_ETNIA_PARDOS, 'Pardos'),
        (TIPO_DECLARACAO_ETNIA_BRANCOS, 'Brancos'),
        (TIPO_DECLARACAO_ETNIA_INDIOS, 'Índios'),
        (TIPO_DECLARACAO_ETNIA_ORIENTAIS, 'Orientais'),
        (TIPO_DECLARACAO_ETNIA_OUTROS, 'Outros')
    )
    tipo_declaracao_etnia = models.IntegerField('Etnia', choices=tipo_declaracao_etnia_choices)
    outros = models.CharField('Outros', max_length=30, blank=True, null=True)
    quantidade = models.IntegerField('Quantos?')

    def __str__(self):
        return '%s - %s' % (self.tipo_declaracao_etnia_choices[self.tipo_declaracao_etnia], self.quantidade)

    class Meta:
        verbose_name = 'Auto declaração'
        verbose_name_plural = '5. Quantos moradores se declaram'


class EstruturaOrganizativa(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='estruturasOrganizativas',
                             on_delete=models.CASCADE)

    TIPO_ESTRUTURA_ORGANIZATIVA_ASSOCIACAO_COMUNITARIA = 10
    TIPO_ESTRUTURA_ORGANIZATIVA_COOPERATIVAS_PRODUCAO_CREDITOS = 20
    TIPO_ESTRUTURA_ORGANIZATIVA_ASSOCIACAO_OU_GRUPOS_DE_MULHERES = 30
    TIPO_ESTRUTURA_ORGANIZATIVA_NUCLEOS_DE_BASE_LIGADOS_AOS_MOVIMENTOS = 40
    TIPO_ESTRUTURA_ORGANIZATIVA_TRABALHOS_COLETIVOS_MULTIROES = 50
    TIPO_ESTRUTURA_ORGANIZATIVA_GRUPOS_VINCULADOS_A_IGREJA = 60
    TIPO_ESTRUTURA_ORGANIZATIVA_GRUPOS_DE_JOVENS = 70
    TIPO_ESTRUTURA_ORGANIZATIVA_GRUPOS_DE_SAUDE = 80
    TIPO_ESTRUTURA_ORGANIZATIVA_ASSOCIACAO_DE_PAIS_E_MESTRES = 90
    TIPO_ESTRUTURA_ORGANIZATIVA_GRUPOS_DE_LASER_E_CULTURA = 100

    tipo_estrutura_organizativa_choices = Choices(
        (TIPO_ESTRUTURA_ORGANIZATIVA_ASSOCIACAO_COMUNITARIA, 'Associação comunitária'),
        (TIPO_ESTRUTURA_ORGANIZATIVA_COOPERATIVAS_PRODUCAO_CREDITOS, 'Cooperativas (produção, créditos, etc.)'),
        (TIPO_ESTRUTURA_ORGANIZATIVA_ASSOCIACAO_OU_GRUPOS_DE_MULHERES, 'Associação ou grupos de mulheres'),
        (TIPO_ESTRUTURA_ORGANIZATIVA_NUCLEOS_DE_BASE_LIGADOS_AOS_MOVIMENTOS, 'Núcleos de base ligados aos movimentos'),
        (TIPO_ESTRUTURA_ORGANIZATIVA_TRABALHOS_COLETIVOS_MULTIROES, 'Trabalhos coletivos (ajuda mútua) "multirões"'),
        (TIPO_ESTRUTURA_ORGANIZATIVA_GRUPOS_VINCULADOS_A_IGREJA, 'Grupos vinculados à igreja (pastoral, etc.)'),
        (TIPO_ESTRUTURA_ORGANIZATIVA_GRUPOS_DE_JOVENS, 'Grupos de jovens'),
        (TIPO_ESTRUTURA_ORGANIZATIVA_GRUPOS_DE_SAUDE, 'Grupos de saúde (pastoral, farmácia viva)'),
        (TIPO_ESTRUTURA_ORGANIZATIVA_ASSOCIACAO_DE_PAIS_E_MESTRES, 'Associação de pais e mestres e outros'),
        (TIPO_ESTRUTURA_ORGANIZATIVA_GRUPOS_DE_LASER_E_CULTURA, 'Grupos de laser e cultura')
    )
    tipo_estrutura_organizativa = models.IntegerField('Estrutura organizativa',
                                                      choices=tipo_estrutura_organizativa_choices)

    FREQUENCIA_FREQUENTE = 10
    FREQUENCIA_REGULARMENTE = 20
    FREQUENCIA_RARAMENTE = 30
    FREQUENCIA_NAO_PARTICIPA = 40

    frequencia_choices = Choices(
        (FREQUENCIA_FREQUENTE, 'Frequente (>70%)'),
        (FREQUENCIA_REGULARMENTE, 'Regularmente (50% a 70%)'),
        (FREQUENCIA_RARAMENTE, 'Raramente (<50%)'),
        (FREQUENCIA_NAO_PARTICIPA, 'Não Participa'),
    )
    frequencia = models.IntegerField('Frequência', choices=frequencia_choices)

    def __str__(self):
        return '%s - %s' % (self.tipo_estrutura_organizativa_choices[self.tipo_estrutura_organizativa], self.frequencia_choices[self.frequencia])

    class Meta:
        verbose_name = 'Estruturas organizativa'
        verbose_name_plural = '6. Das estruturas organizativas internas ao assentamento diga qual existe no assentamento e de quais os membros da família participam'


class FonteAgua(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='fontesAgua', on_delete=models.CASCADE)

    FONTE_DE_AGUA_POCO_ARTESIANO = 10
    FONTE_DE_AGUA_NASCENTE_OU_VERTENTE = 20
    FONTE_DE_AGUA_CORREGOS_OU_RIOS = 30
    FONTE_DE_AGUA_CAPITACAO_DE_AGUA_DA_CHUVA = 40
    FONTE_DE_AGUA_ACUDE_BARREIRO = 50
    FONTE_DE_AGUA_POCO_COMUM = 60
    FONTE_DE_AGUA_DEPOSITO_COLETIVO = 70
    FONTE_DE_AGUA_REDE_DE_AGUA_ENCANADA = 80
    FONTE_DE_AGUA_OUTRA = 90

    fonte_agua_choices = Choices(
        (FONTE_DE_AGUA_POCO_ARTESIANO, 'Poço artesiano'),
        (FONTE_DE_AGUA_NASCENTE_OU_VERTENTE, 'Nascente ou vertente'),
        (FONTE_DE_AGUA_CORREGOS_OU_RIOS, 'Córregos ou Rios'),
        (FONTE_DE_AGUA_CAPITACAO_DE_AGUA_DA_CHUVA, 'Capitação de água da chuva'),
        (FONTE_DE_AGUA_ACUDE_BARREIRO, 'Açude / Barreiro'),
        (FONTE_DE_AGUA_POCO_COMUM, 'Poço comum'),
        (FONTE_DE_AGUA_DEPOSITO_COLETIVO, 'Depósito coletivo'),
        (FONTE_DE_AGUA_REDE_DE_AGUA_ENCANADA, 'Rede de água encanada'),
        (FONTE_DE_AGUA_OUTRA, 'Outra')
    )
    fonte_agua = models.IntegerField('Fonte de água', choices=fonte_agua_choices)
    outra = models.CharField('Outra (Especificar)', max_length=30, blank=True, null=True)

    def __str__(self):
        retorno = self.fonte_agua_choices[self.fonte_agua]
        if self.outra:
            retorno = retorno + '(' + self.outra + ')'
        return retorno

    class Meta:
        verbose_name = ''
        verbose_name_plural = '11. De onde vem a água que abastece a família?'


class TratamentoAgua(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='tratamentosAgua', on_delete=models.CASCADE)

    TRATAMENTO_AGUA_NAO_HA_TRATAMENTO = 10
    TRATAMENTO_AGUA_CLORACAO = 20
    TRATAMENTO_AGUA_FERVURA = 30
    TRATAMENTO_AGUA_FILTRAGEM = 40
    TRATAMENTO_AGUA_DESSALINIZACAO = 50
    TRATAMENTO_AGUA_OUTRA = 60

    tratamento_agua_choices = Choices(
        (TRATAMENTO_AGUA_NAO_HA_TRATAMENTO, 'Não há tratamento'),
        (TRATAMENTO_AGUA_CLORACAO, 'Cloração'),
        (TRATAMENTO_AGUA_FERVURA, 'Fervura'),
        (TRATAMENTO_AGUA_FILTRAGEM, 'Filtragem'),
        (TRATAMENTO_AGUA_DESSALINIZACAO, 'Dessalinização'),
        (TRATAMENTO_AGUA_OUTRA, 'Outros')
    )
    tratamento_agua = models.IntegerField('Forma de tratamento', choices=tratamento_agua_choices)
    outros = models.CharField('Outros (Especificar)', max_length=30, blank=True, null=True)

    def __str__(self):
        retorno = self.tratamento_agua_choices[self.tratamento_agua]
        if self.outros:
            retorno = retorno + ' - ' + self.outros
        return retorno

    class Meta:
        verbose_name = ''
        verbose_name_plural = '12. Qual a forma tratamento da água para consumo?'


class ConstrucaoLote(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='construcoesLote', on_delete=models.CASCADE)

    CONSTRUCAO_NO_LOTE_GALPAO = 10
    CONSTRUCAO_NO_LOTE_CURRAL = 20
    CONSTRUCAO_NO_LOTE_CHIQUEIRO = 30
    CONSTRUCAO_NO_LOTE_GALINHEIRO = 40
    CONSTRUCAO_NO_LOTE_SEGUNDA_CASA = 50
    CONSTRUCAO_NO_LOTE_REPRESA = 60
    CONSTRUCAO_NO_LOTE_ESPACO_PARA_CULTOS_RELIGIOSOS = 70
    CONSTRUCAO_NO_LOTE_ESTABELECIMENTO_COMERCIAL = 80
    CONSTRUCAO_NO_LOTE_AGROINDUSTRIA = 90
    CONSTRUCAO_NO_LOTE_OUTROS = 100

    construcao_no_lote_choices = Choices(
        (CONSTRUCAO_NO_LOTE_GALPAO, 'Galpão'),
        (CONSTRUCAO_NO_LOTE_CURRAL, 'Curral'),
        (CONSTRUCAO_NO_LOTE_CHIQUEIRO, 'Chiqueiro'),
        (CONSTRUCAO_NO_LOTE_GALINHEIRO, 'Galinheiro'),
        (CONSTRUCAO_NO_LOTE_SEGUNDA_CASA, 'Segunda casa'),
        (CONSTRUCAO_NO_LOTE_REPRESA, 'Represa'),
        (CONSTRUCAO_NO_LOTE_ESPACO_PARA_CULTOS_RELIGIOSOS, 'Espaço para cultos religiosos'),
        (CONSTRUCAO_NO_LOTE_ESTABELECIMENTO_COMERCIAL, 'Estabelecimento comercial'),
        (CONSTRUCAO_NO_LOTE_AGROINDUSTRIA, 'Agroindústria'),
        (CONSTRUCAO_NO_LOTE_OUTROS, 'Outros')
    )
    construcao_no_lote = models.IntegerField('Construção', choices=construcao_no_lote_choices)
    outros = models.CharField('Outros', max_length=30, blank=True, null=True)
    quantidade = models.IntegerField('Quantidade')

    def __str__(self):
        retorno = ''
        if self.outros:
            retorno = '{} ({}) - {}'.format(self.construcao_no_lote_choices[self.construcao_no_lote], self.outros, self.quantidade)
        retorno = '{} - {}'.format(self.construcao_no_lote_choices[self.construcao_no_lote], self.quantidade)
        return retorno

    class Meta:
        verbose_name = 'Construção'
        verbose_name_plural = '21. O que tem construído no lote?'


class BemProdutivo(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='bensProdutivos', on_delete=models.CASCADE)

    BEM_PRODUTIVO_TRATOR = 10
    BEM_PRODUTIVO_CAMINHAO = 20
    BEM_PRODUTIVO_CAMINHONETE = 30
    BEM_PRODUTIVO_ARADO_GRADE = 40
    BEM_PRODUTIVO_PLANTADEIRA_ADUBADEIRA = 50
    BEM_PRODUTIVO_PULVERIZADOR_TRATORIZADO = 60
    BEM_PRODUTIVO_CARROCA_OU_CARRO_DE_BOI = 70
    BEM_PRODUTIVO_ARADO_DE_TRACAO_ANIMAL = 80
    BEM_PRODUTIVO_TRITURADOR = 90
    BEM_PRODUTIVO_RESFRIADOR_DE_LEITE = 100
    BEM_PRODUTIVO_COCHOS = 110
    BEM_PRODUTIVO_CALCARIADORA = 120
    BEM_PRODUTIVO_BOMBA_PULVERIZADOR_COSTAL = 130
    BEM_PRODUTIVO_MATRACA = 140
    BEM_PRODUTIVO_BRETE_VACINACAO_GADO = 150
    BEM_PRODUTIVO_ROCADEIRA = 160
    BEM_PRODUTIVO_MOTOSSERRA = 170
    BEM_PRODUTIVO_OUTROS = 180

    bem_produtivo_choices = Choices(
        (BEM_PRODUTIVO_TRATOR, 'Trator'),
        (BEM_PRODUTIVO_CAMINHAO, 'Caminhão'),
        (BEM_PRODUTIVO_CAMINHONETE, 'Caminhonete'),
        (BEM_PRODUTIVO_ARADO_GRADE, 'Arado / grade'),
        (BEM_PRODUTIVO_PLANTADEIRA_ADUBADEIRA, 'Plantadeira / adubadeira'),
        (BEM_PRODUTIVO_PULVERIZADOR_TRATORIZADO, 'Pulverizador "tratorizado"'),
        (BEM_PRODUTIVO_CARROCA_OU_CARRO_DE_BOI, 'Carroça ou carro de boi'),
        (BEM_PRODUTIVO_ARADO_DE_TRACAO_ANIMAL, 'Arado de tração animal'),
        (BEM_PRODUTIVO_TRITURADOR, 'Triturador'),
        (BEM_PRODUTIVO_RESFRIADOR_DE_LEITE, 'Resfriador de leite'),
        (BEM_PRODUTIVO_COCHOS, 'Cochos'),
        (BEM_PRODUTIVO_CALCARIADORA, 'Calcariadora'),
        (BEM_PRODUTIVO_BOMBA_PULVERIZADOR_COSTAL, 'Bomba (pulverizador costal)'),
        (BEM_PRODUTIVO_MATRACA, 'Matraca'),
        (BEM_PRODUTIVO_BRETE_VACINACAO_GADO, 'Brete (vacinação gado)'),
        (BEM_PRODUTIVO_ROCADEIRA, 'Roçadeira'),
        (BEM_PRODUTIVO_MOTOSSERRA, 'Motosserra'),
        (BEM_PRODUTIVO_OUTROS, 'Outros')
    )
    bem_produtivo = models.IntegerField('Bem produtivo', choices=bem_produtivo_choices)
    outros = models.CharField('Outros', max_length=30, blank=True, null=True)
    quantidade = models.IntegerField('Quantidade')

    def __str__(self):
        retorno = ''
        if self.outros:
            retorno = '{} ({}) - {}'.format(self.bem_produtivo_choices[self.bem_produtivo], self.outros,
                                            self.quantidade)
        retorno = '{} - {}'.format(self.bem_produtivo_choices[self.bem_produtivo], self.quantidade)
        return retorno

    class Meta:
        verbose_name = 'Bem produtivo'
        verbose_name_plural = '22. Bens produtivos disponíveis no lote'


class AplicacaoCredito(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='aplicacoesCredito', on_delete=models.CASCADE)

    TIPO_APLICACAO_CREDITO_APOIO_INICIAL_ANTES_DE_2015 = 10
    TIPO_APLICACAO_CREDITO_APOIO_INICIAL_I_APOS_2015 = 20
    TIPO_APLICACAO_CREDITO_APOIO_INICIAL_II_APOS_2015 = 30
    TIPO_APLICACAO_CREDITO_FOMENTO = 40
    TIPO_APLICACAO_CREDITO_FOMENTO_MULHER = 50
    TIPO_APLICACAO_CREDITO_MORADIA = 60
    TIPO_APLICACAO_CREDITO_PNHR_MINHA_CASA_MINHA_VIDA = 70
    TIPO_APLICACAO_CREDITO_REFORMA_MORADIA = 80
    TIPO_APLICACAO_CREDITO_PNHR_REFORMA = 90

    tipo_aplicacao_credito_choices = Choices(
        (TIPO_APLICACAO_CREDITO_APOIO_INICIAL_ANTES_DE_2015, 'Apoio inicial (antes de 2015)'),
        (TIPO_APLICACAO_CREDITO_APOIO_INICIAL_I_APOS_2015, 'Apoio inicial I (após 2015)'),
        (TIPO_APLICACAO_CREDITO_APOIO_INICIAL_II_APOS_2015, 'Apoio inicial II (após 2015)'),
        (TIPO_APLICACAO_CREDITO_FOMENTO, 'Fomento'),
        (TIPO_APLICACAO_CREDITO_FOMENTO_MULHER, 'Fomento Mulher'),
        (TIPO_APLICACAO_CREDITO_MORADIA, 'Moradia'),
        (TIPO_APLICACAO_CREDITO_PNHR_MINHA_CASA_MINHA_VIDA, 'PNHR-Minha Casa Minha Vida'),
        (TIPO_APLICACAO_CREDITO_REFORMA_MORADIA, 'Reforma Moradia'),
        (TIPO_APLICACAO_CREDITO_PNHR_REFORMA, 'PNHR-Reforma')
    )
    tipo_aplicacao_credito = models.IntegerField('Tipo de crédito', choices=tipo_aplicacao_credito_choices)
    valor = models.DecimalField('Valor (R$)', max_digits=10, decimal_places=2)

    def __str__(self):
        return '{} - R$ {}'.format(self.tipo_aplicacao_credito_choices[self.tipo_aplicacao_credito], self.valor)

    class Meta:
        verbose_name = ''
        verbose_name_plural = '23. Com relação aos créditos, como está a aplicação no lote?'


class CreditoBancario(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='creditosBancarios', on_delete=models.CASCADE)

    CREDITO_BANCARIO_MICRO_CREDITO_PRODUTIVO_A = 10
    CREDITO_BANCARIO_A = 20
    CREDITO_BANCARIO_A_C = 30
    CREDITO_BANCARIO_JOVEM = 40
    CREDITO_BANCARIO_MULHER = 50
    CREDITO_BANCARIO_RECUPERACAO_COMPLEMENTAR = 60
    CREDITO_BANCARIO_OUTROS = 70

    credito_bancario_choices = Choices(
        (CREDITO_BANCARIO_MICRO_CREDITO_PRODUTIVO_A, 'Micro Crédito Produtivo (A)'),
        (CREDITO_BANCARIO_A, 'A'),
        (CREDITO_BANCARIO_A_C, 'A/C'),
        (CREDITO_BANCARIO_JOVEM, 'Jovem'),
        (CREDITO_BANCARIO_MULHER, 'Mulher'),
        (CREDITO_BANCARIO_RECUPERACAO_COMPLEMENTAR, 'Recuperação (Complementar)'),
        (CREDITO_BANCARIO_OUTROS, 'Outros')
    )
    credito_bancario = models.IntegerField('Tipo de crédito', choices=credito_bancario_choices)
    outros = models.CharField('Outros', max_length=30, blank=True, null=True)
    valor = models.DecimalField('Valor (R$)', max_digits=10, decimal_places=2)

    CHOICE_SIM = 1
    CHOICE_NAO = 0

    sim_nao_choices = Choices(
        (CHOICE_SIM, 'Sim'),
        (CHOICE_NAO, 'Não')
    )
    adimplente = models.IntegerField('Adimplente?', choices=sim_nao_choices)

    def __str__(self):
        retorno = ''
        if self.outros:
            retorno = '{} ({}) - R$ {} - Adimplente: {}'.format(self.credito_bancario_choices[self.credito_bancario], self.outros, self.valor, self.sim_nao_choices[self.adimplente])
        retorno = '{} - R$ {} - Adimplente: {}'.format(self.credito_bancario_choices[self.credito_bancario], self.valor, self.sim_nao_choices[self.adimplente])
        return retorno

    class Meta:
        verbose_name = ''
        verbose_name_plural = '24. Com relação aos créditos bancários, como está a aplicação na parcela?'


class ProducaoVegetal(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='producoesVegetais', on_delete=models.CASCADE)

    CLASSIFICACAO_CULTURA = 1
    CLASSIFICACAO_OLERICULTURA = 2
    CLASSIFICACAO_FRUTICULTURA = 3
    classificacao = models.IntegerField('Classificação')

    TIPO_PRODUCAO_AMENDOIM = 10
    TIPO_PRODUCAO_ARROZ = 20
    TIPO_PRODUCAO_BATATA_DOCE = 30
    TIPO_PRODUCAO_CANA_DE_ACUCAR = 40
    TIPO_PRODUCAO_FEIJAO = 50
    TIPO_PRODUCAO_MAMONA = 60
    TIPO_PRODUCAO_MANDIOCA_DE_FARINHA = 70
    TIPO_PRODUCAO_MANDIOCA_DE_MESA = 80
    TIPO_PRODUCAO_MILHO = 90

    CULTURA = Choices(
            (TIPO_PRODUCAO_AMENDOIM, 'Amendoim'),
               (TIPO_PRODUCAO_ARROZ, 'Arroz'),
               (TIPO_PRODUCAO_BATATA_DOCE, 'Batata-doce'),
               (TIPO_PRODUCAO_CANA_DE_ACUCAR, 'Cana-de-Açúcar'),
               (TIPO_PRODUCAO_FEIJAO, 'Feijão'),
               (TIPO_PRODUCAO_MAMONA, 'Mamona'),
               (TIPO_PRODUCAO_MANDIOCA_DE_FARINHA, 'Mandioca de / Farinha'),
               (TIPO_PRODUCAO_MANDIOCA_DE_MESA, 'Mandioca de / Mesa'),
               (TIPO_PRODUCAO_MILHO, 'Milho'))

    TIPO_PRODUCAO_ALFACE = 100
    TIPO_PRODUCAO_CEBOLINHA = 110
    TIPO_PRODUCAO_COUVE = 120
    TIPO_PRODUCAO_COENTRO = 130
    TIPO_PRODUCAO_COUVE_FLOR = 140
    TIPO_PRODUCAO_RABANETE = 150
    TIPO_PRODUCAO_RUCULA = 160
    TIPO_PRODUCAO_SALSA = 170
    TIPO_PRODUCAO_ABOBORA = 180
    TIPO_PRODUCAO_MAXIXE = 190
    TIPO_PRODUCAO_MELANCIA = 200
    TIPO_PRODUCAO_MELAO = 210
    TIPO_PRODUCAO_PEPINO = 220
    TIPO_PRODUCAO_PIMENTAO = 230
    TIPO_PRODUCAO_QUIABO = 240
    TIPO_PRODUCAO_TOMATE = 250

    OLERICULTURA = Choices(
        (TIPO_PRODUCAO_ALFACE, 'Alface'),
        (TIPO_PRODUCAO_CEBOLINHA, 'Cebolinha'),
        (TIPO_PRODUCAO_COUVE, 'Couve'),
        (TIPO_PRODUCAO_COENTRO, 'Coentro'),
        (TIPO_PRODUCAO_COUVE_FLOR, 'Couve-flor'),
        (TIPO_PRODUCAO_RABANETE, 'Rabanete'),
        (TIPO_PRODUCAO_RUCULA, 'Rúcula'),
        (TIPO_PRODUCAO_SALSA, 'Salsa'),
        (TIPO_PRODUCAO_ABOBORA, 'Abóbora'),
        (TIPO_PRODUCAO_MAXIXE, 'Maxixe'),
        (TIPO_PRODUCAO_MELANCIA, 'Melancia'),
        (TIPO_PRODUCAO_MELAO, 'Melão'),
        (TIPO_PRODUCAO_PEPINO, 'Pepino'),
        (TIPO_PRODUCAO_PIMENTAO, 'Pimentão'),
        (TIPO_PRODUCAO_QUIABO, 'Quiabo'),
        (TIPO_PRODUCAO_TOMATE, 'Tomate')
    )

    TIPO_PRODUCAO_ABACATE = 260
    TIPO_PRODUCAO_ACEROLA = 270
    TIPO_PRODUCAO_BANANA = 280
    TIPO_PRODUCAO_CAJU = 290
    TIPO_PRODUCAO_COCO = 300
    TIPO_PRODUCAO_GOIABA = 310
    TIPO_PRODUCAO_JABUTICABA = 320
    TIPO_PRODUCAO_JACA = 330
    TIPO_PRODUCAO_LARANJA = 340
    TIPO_PRODUCAO_LIMA = 350
    TIPO_PRODUCAO_LIMAO = 360
    TIPO_PRODUCAO_MANGA = 370
    TIPO_PRODUCAO_MARACUJA = 380
    TIPO_PRODUCAO_TAMARINDO = 390
    TIPO_PRODUCAO_TANGERINA = 400
    TIPO_PRODUCAO_UVA = 410

    FRUTICULTURA = Choices(
        (TIPO_PRODUCAO_ABACATE, 'Abacate'),
        (TIPO_PRODUCAO_ACEROLA, 'Acerola'),
        (TIPO_PRODUCAO_BANANA, 'Banana'),
        (TIPO_PRODUCAO_CAJU, 'Cajú'),
        (TIPO_PRODUCAO_COCO, 'Côco'),
        (TIPO_PRODUCAO_GOIABA, 'Goiaba'),
        (TIPO_PRODUCAO_JABUTICABA, 'Jabuticaba'),
        (TIPO_PRODUCAO_JACA, 'Jaca'),
        (TIPO_PRODUCAO_LARANJA, 'Laranja'),
        (TIPO_PRODUCAO_LIMA, 'Lima'),
        (TIPO_PRODUCAO_LIMAO, 'Limão'),
        (TIPO_PRODUCAO_MANGA, 'Manga'),
        (TIPO_PRODUCAO_MARACUJA, 'Maracujá'),
        (TIPO_PRODUCAO_TAMARINDO, 'Tamarindo'),
        (TIPO_PRODUCAO_TANGERINA, 'Tangerina'),
        (TIPO_PRODUCAO_UVA, 'Uva')
    )

    TIPO_PRODUCAO_OUTROS = 999

    tipo_producao_choices = CULTURA + OLERICULTURA + FRUTICULTURA + (
        (TIPO_PRODUCAO_OUTROS, 'Outros'),
    )
    tipo_producao = models.IntegerField('Tipo de produção', choices=tipo_producao_choices)
    tipo_producao_outros = models.CharField('Tipo de produção (Outros)', max_length=30, blank=True, null=True)
    area_plantada = models.DecimalField('Área plantada', max_digits=10, decimal_places=4)

    MEDIDA_HA = 1
    MEDIDA_M2 = 2

    medida_choices = (
        (MEDIDA_HA, 'ha'),
        (MEDIDA_M2, 'm2')
    )
    medida_area_plantada = models.IntegerField('Medida da área plantada', choices=medida_choices)
    producao_consumo = models.FloatField('Produção (Consumo)', blank=True, null=True)
    producao_comercio = models.FloatField('Produção (Comércio)', blank=True, null=True)

    UNIDADE_MEDIDA_KG = 1
    UNIDADE_MEDIDA_UN = 2

    unidade_medida_choices = Choices(
        (UNIDADE_MEDIDA_KG, 'Kg'),
        (UNIDADE_MEDIDA_UN, 'un')
    )
    producao_unidade_medida = models.IntegerField(
        'Unidade de medida da produção', choices=unidade_medida_choices, blank=True, null=True
    )
    valor = models.DecimalField('Valor (R$)', max_digits=10, decimal_places=4, blank=True, null=True)

    IRRIGACAO_SIM = 1
    IRRIGACAO_NAO = 0

    irrigacao_choices = Choices(
        (IRRIGACAO_SIM, 'Sim'),
        (IRRIGACAO_NAO, 'Não')
    )
    irrigacao = models.IntegerField('Plantio irrigado?', choices=irrigacao_choices, blank=True, null=True)
    area_irrigada = models.DecimalField('Área irrigada', max_digits=10, decimal_places=4, blank=True, null=True)
    medida_area_irrigada = models.IntegerField('Medida da área irrigada', choices=medida_choices, blank=True, null=True)

    TIPO_IRRIGACAO_ASPERSAO = 10
    TIPO_IRRIGACAO_SULCO = 20
    TIPO_IRRIGACAO_GOTEJAMENTO = 30
    TIPO_IRRIGACAO_OUTROS = 40

    tipo_irrigacao_choices = Choices(
        (TIPO_IRRIGACAO_ASPERSAO, 'Aspersão'),
        (TIPO_IRRIGACAO_SULCO, 'Sulco'),
        (TIPO_IRRIGACAO_GOTEJAMENTO, 'Gotejamento'),
        (TIPO_IRRIGACAO_OUTROS, 'Outros')
    )
    tipo_irrigacao = models.IntegerField('Tipo de irrigação', choices=tipo_irrigacao_choices, blank=True, null=True)

    CANAL_COMERCIALIZACAO_VENDA_DIRETA_AO_CONSUMIDOR = 10
    CANAL_COMERCIALIZACAO_VENDA_EM_FEIRAS = 20
    CANAL_COMERCIALIZACAO_ENTREGA_PARA_SUPERMERCADOS_MERCEARIAS_AÇOUGUES = 30
    CANAL_COMERCIALIZACAO_VENDA_PARA_INDUSTRIAS_AGROINDUSTRIAS_LATICINIOS = 40
    CANAL_COMERCIALIZACAO_VENDA_PARA_AGENTES_ATRAVESSADORES = 50
    CANAL_COMERCIALIZACAO_OUTROS = 60

    canal_comercializacao_choices = Choices(
        (CANAL_COMERCIALIZACAO_VENDA_DIRETA_AO_CONSUMIDOR, 'Venda direta ao consumidor (de casa em casa)'),
        (CANAL_COMERCIALIZACAO_VENDA_EM_FEIRAS, 'Venda em feiras'),
        (CANAL_COMERCIALIZACAO_ENTREGA_PARA_SUPERMERCADOS_MERCEARIAS_AÇOUGUES, 'Entrega para supermercados, mercearias, açougues, etc'),
        (CANAL_COMERCIALIZACAO_VENDA_PARA_INDUSTRIAS_AGROINDUSTRIAS_LATICINIOS, 'Venda p/ indústrias, e/ou agroindústrias (laticínios etc'),
        (CANAL_COMERCIALIZACAO_VENDA_PARA_AGENTES_ATRAVESSADORES, 'Venda para agentes "atravessadores"'),
        (CANAL_COMERCIALIZACAO_OUTROS, 'Outros')
    )
    canal_comercializacao = models.IntegerField('Formas/Canais de Comercialização', choices=canal_comercializacao_choices, blank=True, null=True)

    MERCADO_INSTITUCIONAL_PAA_CONAB = 10
    MERCADO_INSTITUCIONAL_PAA_PREFEITURA_MDS = 20
    MERCADO_INSTITUCIONAL_ALIMENTACAO_ESCOLAR_PNAE = 30
    MERCADO_INSTITUCIONAL_BIODIESEL = 40
    MERCADO_INSTITUCIONAL_OUTROS = 50

    mercado_institucional_choices = Choices(
        (MERCADO_INSTITUCIONAL_PAA_CONAB, 'PAA-CONAB'),
        (MERCADO_INSTITUCIONAL_PAA_PREFEITURA_MDS, 'PAA-Prefeitura / MDS'),
        (MERCADO_INSTITUCIONAL_ALIMENTACAO_ESCOLAR_PNAE, 'Alimentação Escolar - PNAE'),
        (MERCADO_INSTITUCIONAL_BIODIESEL, 'Biodiesel'),
        (MERCADO_INSTITUCIONAL_OUTROS, 'Outros')
    )
    mercado_institucional = models.IntegerField('Mercado Institucional', choices=mercado_institucional_choices, blank=True, null=True)


class CulturaManager(models.Manager):
    def get_queryset(self):
        return super(CulturaManager, self).get_queryset().filter(classificacao=Cultura.CLASSIFICACAO_CULTURA)


class Cultura(ProducaoVegetal):
    objects = CulturaManager()

    def __str__(self):
        retorno = ''
        if self.medida_area_plantada == self.MEDIDA_HA:
            retorno = '{} - {}ha'.format(self.tipo_producao_choices[self.tipo_producao], self.area_plantada)
        retorno = '{} - {}m2'.format(self.tipo_producao_choices[self.tipo_producao], self.area_plantada)
        return retorno

    def save(self, *args, **kwargs):
        self.classificacao = self.CLASSIFICACAO_CULTURA
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = ''
        verbose_name_plural = '25. Agora falaremos sobre a produção/culturas, plantadas na sua lavoura/roça no último ano agrícola'


class OlericulturaManager(models.Manager):
    def get_queryset(self):
        return super(OlericulturaManager, self).get_queryset().filter(classificacao=Olericultura.CLASSIFICACAO_OLERICULTURA)


class Olericultura(ProducaoVegetal):
    objects = OlericulturaManager()

    def __str__(self):
        retorno = ''
        if self.medida_area_plantada == self.MEDIDA_HA:
            retorno = '{} - {}ha'.format(self.tipo_producao_choices[self.tipo_producao], self.area_plantada)
        retorno = '{} - {}m2'.format(self.tipo_producao_choices[self.tipo_producao], self.area_plantada)
        return retorno

    def save(self, *args, **kwargs):
        self.classificacao = self.CLASSIFICACAO_OLERICULTURA
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = ''
        verbose_name_plural = '26. Olericulturas - Legumes e Verduras no último ano agrícola'


class FruticulturaManager(models.Manager):
    def get_queryset(self):
        return super(FruticulturaManager, self).get_queryset().filter(classificacao=Fruticultura.CLASSIFICACAO_FRUTICULTURA)


class Fruticultura(ProducaoVegetal):
    objects = FruticulturaManager()

    def __str__(self):
        retorno = ''
        if self.medida_area_plantada == self.MEDIDA_HA:
            retorno = '{} - {}ha'.format(self.tipo_producao_choices[self.tipo_producao], self.area_plantada)
        retorno = '{} - {}m2'.format(self.tipo_producao_choices[self.tipo_producao], self.area_plantada)
        return retorno

    def save(self, *args, **kwargs):
        self.classificacao = self.CLASSIFICACAO_FRUTICULTURA
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = ''
        verbose_name_plural = '27. Fruticultura referente ao último ano agrícola'


class AtividadeExtrativista(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='atividadesExtrativistas',
                             on_delete=models.CASCADE)

    ESPECIFICACAO_ACAI = 10
    ESPECIFICACAO_BABACU = 20
    ESPECIFICACAO_BURITI = 30
    ESPECIFICACAO_CAGAITA = 40
    ESPECIFICACAO_MURICI = 50
    ESPECIFICACAO_PEQUI = 60
    ESPECIFICACAO_OUTROS = 70

    especificacao_choices = Choices(
        (ESPECIFICACAO_ACAI, 'Açaí(Kg)'),
        (ESPECIFICACAO_BABACU, 'Babaçu(Kg)'),
        (ESPECIFICACAO_BURITI, 'Buriti(Kg)'),
        (ESPECIFICACAO_CAGAITA, 'Cagaita(Kg)'),
        (ESPECIFICACAO_MURICI, 'Murici(Kg)'),
        (ESPECIFICACAO_PEQUI, 'Pequi(Kg)'),
        (ESPECIFICACAO_OUTROS, 'Outros')
    )
    especificacao = models.IntegerField('Especificação', choices=especificacao_choices)
    outros = models.CharField('Outros', max_length=30, blank=True, null=True)
    quantidade_frutos_ano = models.IntegerField('Quantidade Colhida / Ano - Fruto(s)')
    quantidade_palmitos_ano = models.IntegerField('Quantidade Colhida / Ano - Palmito(s)')
    valor = models.DecimalField('Valor R$/Kg', max_digits=10, decimal_places=2)

    CANAL_COMERCIALIZACAO_VENDA_DIRETA_AO_CONSUMIDOR = 10
    CANAL_COMERCIALIZACAO_VENDA_EM_FEIRAS = 20
    CANAL_COMERCIALIZACAO_ENTREGA_PARA_SUPERMERCADOS_MERCEARIAS_AÇOUGUES = 30
    CANAL_COMERCIALIZACAO_VENDA_PARA_INDUSTRIAS_AGROINDUSTRIAS_LATICINIOS = 40
    CANAL_COMERCIALIZACAO_VENDA_PARA_AGENTES_ATRAVESSADORES = 50
    CANAL_COMERCIALIZACAO_OUTROS = 60

    canal_comercializacao_choices = Choices(
        (CANAL_COMERCIALIZACAO_VENDA_DIRETA_AO_CONSUMIDOR, 'Venda direta ao consumidor (de casa em casa)'),
        (CANAL_COMERCIALIZACAO_VENDA_EM_FEIRAS, 'Venda em feiras'),
        (CANAL_COMERCIALIZACAO_ENTREGA_PARA_SUPERMERCADOS_MERCEARIAS_AÇOUGUES,
         'Entrega para supermercados, mercearias, açougues, etc'),
        (CANAL_COMERCIALIZACAO_VENDA_PARA_INDUSTRIAS_AGROINDUSTRIAS_LATICINIOS,
         'Venda p/ indústrias, e/ou agroindústrias (laticínios etc'),
        (CANAL_COMERCIALIZACAO_VENDA_PARA_AGENTES_ATRAVESSADORES, 'Venda para agentes "atravessadores"'),
        (CANAL_COMERCIALIZACAO_OUTROS, 'Outros')
    )
    canal_comercializacao = models.IntegerField('Formas/Canais de Comercialização',
                                                choices=canal_comercializacao_choices, blank=True, null=True)

    MERCADO_INSTITUCIONAL_PAA_CONAB = 10
    MERCADO_INSTITUCIONAL_PAA_PREFEITURA_MDS = 20
    MERCADO_INSTITUCIONAL_ALIMENTACAO_ESCOLAR_PNAE = 30
    MERCADO_INSTITUCIONAL_BIODIESEL = 40
    MERCADO_INSTITUCIONAL_OUTROS = 50

    mercado_institucional_choices = Choices(
        (MERCADO_INSTITUCIONAL_PAA_CONAB, 'PAA-CONAB'),
        (MERCADO_INSTITUCIONAL_PAA_PREFEITURA_MDS, 'PAA-Prefeitura / MDS'),
        (MERCADO_INSTITUCIONAL_ALIMENTACAO_ESCOLAR_PNAE, 'Alimentação Escolar - PNAE'),
        (MERCADO_INSTITUCIONAL_BIODIESEL, 'Biodiesel'),
        (MERCADO_INSTITUCIONAL_OUTROS, 'Outros')
    )
    mercado_institucional = models.IntegerField('Mercado Institucional', choices=mercado_institucional_choices,
                                                blank=True, null=True)

    def __str__(self):
        retorno = ''
        if self.outros:
            retorno = '{} ({}) - {} fruto(s), {} palmito(s)'.format(self.especificacao_choices[self.especificacao], self.outros, self.quantidade_frutos_ano, self.quantidade_palmitos_ano)
        retorno = '{} - {} fruto(s), {} palmito(s)'.format(self.especificacao_choices[self.especificacao], self.quantidade_frutos_ano, self.quantidade_palmitos_ano)
        return retorno

    class Meta:
        verbose_name = ''
        verbose_name_plural = '29. Produtos de atividade extrativista do último ano agrícola'


class ProducaoFlorestal(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='producoesFlorestais', on_delete=models.CASCADE)

    ESPECIFICACAO_EUCALIPTO = 10
    ESPECIFICACAO_TECA = 20
    ESPECIFICACAO_SERINGUEIRA_KG_LATEX = 30
    ESPECIFICACAO_SERINGUEIRA_M3_MADEIRA = 40
    ESPECIFICACAO_OUTROS = 50

    especificacao_choices = Choices(
        (ESPECIFICACAO_EUCALIPTO, 'Eucalipto(m³)'),
        (ESPECIFICACAO_TECA, 'Teca(m³)'),
        (ESPECIFICACAO_SERINGUEIRA_KG_LATEX, 'Seringueira(Kg/látex)'),
        (ESPECIFICACAO_SERINGUEIRA_M3_MADEIRA, 'Seringueira(m³/Madeira)'),
        (ESPECIFICACAO_OUTROS, 'Outros')
    )
    especificacao = models.IntegerField('Especificação', choices=especificacao_choices)
    outros = models.CharField('Outros', max_length=30, blank=True, null=True)
    quantidade_produzida_ano = models.IntegerField('Quantidade produzida/ano')
    area_plantada = models.DecimalField('Área plantada (ha)', max_digits=10, decimal_places=4)
    valor = models.DecimalField('R$/Unidade colhida', max_digits=10, decimal_places=2)

    CANAL_COMERCIALIZACAO_VENDA_DIRETA_AO_CONSUMIDOR = 10
    CANAL_COMERCIALIZACAO_VENDA_EM_FEIRAS = 20
    CANAL_COMERCIALIZACAO_ENTREGA_PARA_SUPERMERCADOS_MERCEARIAS_AÇOUGUES = 30
    CANAL_COMERCIALIZACAO_VENDA_PARA_INDUSTRIAS_AGROINDUSTRIAS_LATICINIOS = 40
    CANAL_COMERCIALIZACAO_VENDA_PARA_AGENTES_ATRAVESSADORES = 50
    CANAL_COMERCIALIZACAO_OUTROS = 60

    canal_comercializacao_choices = Choices(
        (CANAL_COMERCIALIZACAO_VENDA_DIRETA_AO_CONSUMIDOR, 'Venda direta ao consumidor (de casa em casa)'),
        (CANAL_COMERCIALIZACAO_VENDA_EM_FEIRAS, 'Venda em feiras'),
        (CANAL_COMERCIALIZACAO_ENTREGA_PARA_SUPERMERCADOS_MERCEARIAS_AÇOUGUES,
         'Entrega para supermercados, mercearias, açougues, etc'),
        (CANAL_COMERCIALIZACAO_VENDA_PARA_INDUSTRIAS_AGROINDUSTRIAS_LATICINIOS,
         'Venda p/ indústrias, e/ou agroindústrias (laticínios etc'),
        (CANAL_COMERCIALIZACAO_VENDA_PARA_AGENTES_ATRAVESSADORES, 'Venda para agentes "atravessadores"'),
        (CANAL_COMERCIALIZACAO_OUTROS, 'Outros')
    )
    canal_comercializacao = models.IntegerField('Formas/Canais de Comercialização',
                                                choices=canal_comercializacao_choices, blank=True, null=True)



    def __str__(self):
        retorno = ''
        if self.outros:
            retorno = '{} ({}) - {}'.format(self.especificacao_choices[self.especificacao], self.outros,
                                            self.quantidade_produzida_ano)
        retorno = '{} - {}'.format(self.especificacao_choices[self.especificacao], self.quantidade_produzida_ano)
        return retorno

    class Meta:
        verbose_name = ''
        verbose_name_plural = '30. Produção Florestal do último ano agrícola'


class ProducaoAnimal(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='producoesAnimais', on_delete=models.CASCADE)

    CLASSIFICACAO_BOVINOCULTURA = 1
    CLASSIFICACAO_OUTRA_CRIACAO = 2

    classificacao = models.IntegerField('Classificação')

    TIPO_CRIACAO_GADO_LEITEIRO = 1
    TIPO_CRIACAO_GADO_DE_CORTE = 2
    TIPO_CRIACAO_OUTROS = 99

    tipo_criacao_choices = Choices(
        (TIPO_CRIACAO_GADO_LEITEIRO, 'Gado Leiteiro'),
        (TIPO_CRIACAO_GADO_DE_CORTE, 'Gado de Corte')
    )
    tipo_criacao = models.IntegerField('Tipo de criação', choices=tipo_criacao_choices)

    ESPECIFICACAO_TOUROS = 10
    ESPECIFICACAO_VACAS = 20
    ESPECIFICACAO_NOVILHAS_MAIS_DE_2_ANOS = 30
    ESPECIFICACAO_NOVILHAS_MAIS_DE_1_ANO = 40
    ESPECIFICACAO_BEZERRAS = 50
    ESPECIFICACAO_BOI = 60

    BOVINOCULTURA = Choices((ESPECIFICACAO_TOUROS, 'Touros'),
                     (ESPECIFICACAO_VACAS, 'Vacas'),
                     (ESPECIFICACAO_NOVILHAS_MAIS_DE_2_ANOS, 'Novilhas(os) + de 02 anos'),
                     (ESPECIFICACAO_NOVILHAS_MAIS_DE_1_ANO, 'Novilhas(os) + de 01 ano'),
                     (ESPECIFICACAO_BEZERRAS, 'Bezerras(os)'),
                     (ESPECIFICACAO_BOI, 'Boi'),)

    ESPECIFICACAO_FRANGO_DE_CORTE_CAIPIRA = 70
    ESPECIFICACAO_GALINHA_CAIPIRA_SOMENTE_FRANGOS_E_ADULTOS = 80
    ESPECIFICACAO_SUINOS = 90
    ESPECIFICACAO_OUVINOS = 100
    ESPECIFICACAO_EQUINOS_MUARES = 110
    ESPECIFICACAO_CAPRINOS = 120

    OUTRA_CRIACAO = Choices((ESPECIFICACAO_FRANGO_DE_CORTE_CAIPIRA, 'Frango de corte caipira'),
                     (ESPECIFICACAO_GALINHA_CAIPIRA_SOMENTE_FRANGOS_E_ADULTOS,
                      'Galinha caipira (somente frangos(as) e adultos)'),
                     (ESPECIFICACAO_SUINOS, 'Suínos'),
                     (ESPECIFICACAO_OUVINOS, 'Ovinos'),
                     (ESPECIFICACAO_EQUINOS_MUARES, 'Equinos / Muares'),
                     (ESPECIFICACAO_CAPRINOS, 'Caprinos'),)

    ESPECIFICACAO_OUTROS = 999

    especificacao_choices = BOVINOCULTURA + OUTRA_CRIACAO + (
        (ESPECIFICACAO_OUTROS, 'Outros'),
    )
    especificacao = models.IntegerField('Especificação', choices=especificacao_choices)
    quantidade_cabecas = models.IntegerField('Nº de Cabeça(s)')
    valor_cabeca = models.DecimalField('R$/Cabeça', max_digits=7, decimal_places=2)


class BovinoculturaManager(models.Manager):
    def get_queryset(self):
        return super(BovinoculturaManager, self).get_queryset().filter(classificacao=Bovinocultura.CLASSIFICACAO_BOVINOCULTURA)


class Bovinocultura(ProducaoAnimal):
    objects = BovinoculturaManager()

    def __str__(self):
        return '{} - {}: {} cabeça(s), R$ {} por cabeça'.format(self.tipo_criacao_choices[self.tipo_criacao], self.especificacao_choices[self.especificacao], self.quantidade_cabecas, self.valor_cabeca)

    def save(self, *args, **kwargs):
        self.classificacao = self.CLASSIFICACAO_BOVINOCULTURA
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = ''
        verbose_name_plural = '31. Sobre o Efetivo Animal do último ano agrícola (Bovinocultura)'


class OutraCriacaoManager(models.Manager):
    def get_queryset(self):
        return super(OutraCriacaoManager, self).get_queryset().filter(classificacao=OutraCriacao.CLASSIFICACAO_OUTRA_CRIACAO)


class OutraCriacao(ProducaoAnimal):
    objects = OutraCriacaoManager()

    def __str__(self):
        return '{}: {} cabeça(s), R$ {} por cabeça'.format(self.especificacao_choices[self.especificacao], self.quantidade_cabecas, self.valor_cabeca)

    def save(self, *args, **kwargs):
        self.classificacao = self.CLASSIFICACAO_OUTRA_CRIACAO
        self.tipo_criacao = self.TIPO_CRIACAO_OUTROS
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = ''
        verbose_name_plural = '31. Sobre o Efetivo Animal do último ano agrícola (Outras Criações)'


class DescarteAnimal(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='descartesAnimais', on_delete=models.CASCADE)

    TIPO_CRIACAO_GADO_LEITEIRO = 1
    TIPO_CRIACAO_GADO_DE_CORTE = 2
    TIPO_CRIACAO_OUTROS = 99

    tipo_criacao = models.IntegerField('Tipo de criação')

    ESPECIFICACAO_TOUROS = 10
    ESPECIFICACAO_VACAS = 20
    ESPECIFICACAO_NOVILHAS_MAIS_DE_2_ANOS = 30
    ESPECIFICACAO_NOVILHAS_MAIS_DE_1_ANO = 40
    ESPECIFICACAO_BEZERRAS = 50
    ESPECIFICACAO_BOI = 60

    especificacao_choices = Choices(
        (ESPECIFICACAO_TOUROS, 'Touros'),
        (ESPECIFICACAO_VACAS, 'Vacas'),
        (ESPECIFICACAO_NOVILHAS_MAIS_DE_2_ANOS, 'Novilhas(os) + de 02 anos'),
        (ESPECIFICACAO_NOVILHAS_MAIS_DE_1_ANO, 'Novilhas(os) + de 01 ano'),
        (ESPECIFICACAO_BEZERRAS, 'Bezerras(os)'),
        (ESPECIFICACAO_BOI, 'Boi')
    )
    especificacao = models.IntegerField('Especificação', choices=especificacao_choices)
    quantidade_cabecas_consumo = models.IntegerField('Nº de Cabeça(s) - Consumo')
    quantidade_cabecas_comercio = models.IntegerField('Nº de Cabeça(s) - Comércio')
    valor_cabeca = models.DecimalField('R$/Cabeça', max_digits=7, decimal_places=2)

    CANAL_COMERCIALIZACAO_VENDA_PARA_OUTRO_PRODUTOR = 10
    CANAL_COMERCIALIZACAO_ENTREGA_PARA_FRIGORIFICO_ACOUGUE = 20
    CANAL_COMERCIALIZACAO_VENDA_PARA_AGENTES_ATRAVESSADORES = 30
    CANAL_COMERCIALIZACAO_OUTROS = 40

    canal_comercializacao_choices = Choices(
        (CANAL_COMERCIALIZACAO_VENDA_PARA_OUTRO_PRODUTOR, 'Venda para outro produtor'),
        (CANAL_COMERCIALIZACAO_ENTREGA_PARA_FRIGORIFICO_ACOUGUE, 'Entrega para frigorífico/açougue'),
        (CANAL_COMERCIALIZACAO_VENDA_PARA_AGENTES_ATRAVESSADORES, 'Venda para agentes "atravessadores"'),
        (CANAL_COMERCIALIZACAO_OUTROS, 'Outros')
    )
    canal_comercializacao = models.IntegerField('Formas/Canais de Comercialização',
                                                choices=canal_comercializacao_choices)
    canal_comercializacao_outros = models.CharField('Outros (Especificar)', max_length=30, blank=True, null=True)


class BovinoculturaLeiteiraManager(models.Manager):
    def get_queryset(self):
        return super(BovinoculturaLeiteiraManager, self).get_queryset().filter(tipo_criacao=BovinoculturaLeiteira.TIPO_CRIACAO_GADO_LEITEIRO)


class BovinoculturaLeiteira(DescarteAnimal):
    objects = BovinoculturaLeiteiraManager()

    def __str__(self):
        return '{} - Consumo: {} cabeça(s), Comércio: {} cabeça(s)'.format(
            self.especificacao_choices[self.especificacao], self.quantidade_cabecas_consumo,
            self.quantidade_cabecas_comercio)

    def save(self, *args, **kwargs):
        self.tipo_criacao = self.TIPO_CRIACAO_GADO_LEITEIRO
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = ''
        verbose_name_plural = 'Descarte Animal - Bovinocultura Leiteira'


class BovinoculturaCorteManager(models.Manager):
    def get_queryset(self):
        return super(BovinoculturaCorteManager, self).get_queryset().filter(tipo_criacao=BovinoculturaCorte.TIPO_CRIACAO_GADO_DE_CORTE)


class BovinoculturaCorte(DescarteAnimal):
    objects = BovinoculturaCorteManager()

    def __str__(self):
        return '{} - Consumo: {} cabeça(s), Comércio: {} cabeça(s)'.format(
            self.especificacao_choices[self.especificacao], self.quantidade_cabecas_consumo,
            self.quantidade_cabecas_comercio)

    def save(self, *args, **kwargs):
        self.tipo_criacao = self.TIPO_CRIACAO_GADO_DE_CORTE
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = ''
        verbose_name_plural = 'Descarte Animal - Bovinocultura de Corte'


class Produto(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='produtosOrigemAnimal', on_delete=models.CASCADE)

    CLASSIFICACAO_ORIGEM_ANIMAL = 1
    CLASSIFICACAO_PROCESSADO_BENEFICIADO = 2

    classificacao = models.IntegerField('Classificação')

    ESPECIFICACAO_CARNE = 10
    ESPECIFICACAO_LEITE = 20
    ESPECIFICACAO_MEL = 30
    ESPECIFICACAO_OVOS = 40
    ESPECIFICACAO_PEIXES = 50

    ORIGEM_ANIMAL = Choices((ESPECIFICACAO_CARNE, 'Carne(Kg)'),
                     (ESPECIFICACAO_LEITE, 'Leite(L)'),
                     (ESPECIFICACAO_MEL, 'Mel(Kg)'),
                     (ESPECIFICACAO_OVOS, 'Ovos(Dz)'),
                     (ESPECIFICACAO_PEIXES, 'Peixes(Kg)'),)

    ESPECIFICACAO_BANHA = 60
    ESPECIFICACAO_CONSERVAS = 70
    ESPECIFICACAO_DOCES = 80
    ESPECIFICACAO_FARINHA_DE_MANDIOCA = 90
    ESPECIFICACAO_LINGUICA = 100
    ESPECIFICACAO_POVILHO_DE_MANDIOCA = 110
    ESPECIFICACAO_QUEIJO = 120
    ESPECIFICACAO_RAPADURA = 130

    PROCESSADO_BENEFICIADO = Choices((ESPECIFICACAO_BANHA, 'Banha(Kg)'),
                              (ESPECIFICACAO_CONSERVAS, 'Conservas(Un)'),
                              (ESPECIFICACAO_DOCES, 'Doces(Un)'),
                              (ESPECIFICACAO_FARINHA_DE_MANDIOCA, 'Farinha Mandioca(Kg'),
                              (ESPECIFICACAO_LINGUICA, 'Linguiça(Kg)'),
                              (ESPECIFICACAO_POVILHO_DE_MANDIOCA, 'Polvilho de Mandioca(Kg)'),
                              (ESPECIFICACAO_QUEIJO, 'Queijo(Kg)'),
                              (ESPECIFICACAO_RAPADURA, 'Rapadura(Kg)'),)

    ESPECIFICACAO_OUTROS = 999

    especificacao_choices = ORIGEM_ANIMAL + PROCESSADO_BENEFICIADO + (
        (ESPECIFICACAO_OUTROS, 'Outros'),
    )
    especificacao = models.IntegerField('Especificação', choices=especificacao_choices)
    outros = models.CharField('Outros (Especificar)', max_length=30, blank=True, null=True)
    producao_consumo = models.IntegerField('Produção (Consumo)')
    producao_comercio = models.IntegerField('Produção (Comércio)')
    valor = models.DecimalField('Valor R$', max_digits=7, decimal_places=2)

    CANAL_COMERCIALIZACAO_VENDA_DIRETA_AO_CONSUMIDOR = 10
    CANAL_COMERCIALIZACAO_VENDA_EM_FEIRAS = 20
    CANAL_COMERCIALIZACAO_ENTREGA_PARA_SUPERMERCADOS_MERCEARIAS_AÇOUGUES = 30
    CANAL_COMERCIALIZACAO_VENDA_PARA_INDUSTRIAS_AGROINDUSTRIAS_LATICINIOS = 40
    CANAL_COMERCIALIZACAO_VENDA_PARA_AGENTES_ATRAVESSADORES = 50
    CANAL_COMERCIALIZACAO_OUTROS = 60

    canal_comercializacao_choices = Choices(
        (CANAL_COMERCIALIZACAO_VENDA_DIRETA_AO_CONSUMIDOR, 'Venda direta ao consumidor (de casa em casa)'),
        (CANAL_COMERCIALIZACAO_VENDA_EM_FEIRAS, 'Venda em feiras'),
        (CANAL_COMERCIALIZACAO_ENTREGA_PARA_SUPERMERCADOS_MERCEARIAS_AÇOUGUES,
         'Entrega para supermercados, mercearias, açougues, etc'),
        (CANAL_COMERCIALIZACAO_VENDA_PARA_INDUSTRIAS_AGROINDUSTRIAS_LATICINIOS,
         'Venda p/ indústrias, e/ou agroindústrias (laticínios etc'),
        (CANAL_COMERCIALIZACAO_VENDA_PARA_AGENTES_ATRAVESSADORES, 'Venda para agentes "atravessadores"'),
        (CANAL_COMERCIALIZACAO_OUTROS, 'Outros')
    )
    canal_comercializacao = models.IntegerField('Formas/Canais de Comercialização',
                                                choices=canal_comercializacao_choices, blank=True, null=True)

    MERCADO_INSTITUCIONAL_PAA_CONAB = 10
    MERCADO_INSTITUCIONAL_PAA_PREFEITURA_MDS = 20
    MERCADO_INSTITUCIONAL_ALIMENTACAO_ESCOLAR_PNAE = 30
    MERCADO_INSTITUCIONAL_BIODIESEL = 40
    MERCADO_INSTITUCIONAL_OUTROS = 50

    mercado_institucional_choices = Choices(
        (MERCADO_INSTITUCIONAL_PAA_CONAB, 'PAA-CONAB'),
        (MERCADO_INSTITUCIONAL_PAA_PREFEITURA_MDS, 'PAA-Prefeitura / MDS'),
        (MERCADO_INSTITUCIONAL_ALIMENTACAO_ESCOLAR_PNAE, 'Alimentação Escolar - PNAE'),
        (MERCADO_INSTITUCIONAL_BIODIESEL, 'Biodiesel'),
        (MERCADO_INSTITUCIONAL_OUTROS, 'Outros')
    )
    mercado_institucional = models.IntegerField('Mercado Institucional', choices=mercado_institucional_choices,
                                                blank=True, null=True)


class OrigemAnimalManager(models.Manager):
    def get_queryset(self):
        return super(OrigemAnimalManager, self).get_queryset().filter(classificacao=OrigemAnimal.CLASSIFICACAO_ORIGEM_ANIMAL)


class OrigemAnimal(Produto):
    objects = OrigemAnimalManager()

    def __str__(self):
        return '{} - Consumo: {}, Comércio: {}'.format(self.especificacao_choices[self.especificacao], self.producao_consumo, self.producao_comercio)

    def save(self, *args, **kwargs):
        self.classificacao = self.CLASSIFICACAO_ORIGEM_ANIMAL
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = ''
        verbose_name_plural = '32. Sobre os produtos de origem animal produzidos no último ano agrícola'


class NivelTecnologicoProducaoAnimal(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='niveisTecnologicosProducaoAnimal', on_delete=models.CASCADE)

    CHOICE_SIM = 1
    CHOICE_NAO = 0

    TIPO_CAPINEIRA_CANA = 10
    TIPO_CAPINEIRA_NAPIER = 20
    TIPO_CAPINEIRA_NAO_SE_APLICA = 99

    tipo_capineira_choices = Choices(
        (TIPO_CAPINEIRA_CANA, 'Cana'),
        (TIPO_CAPINEIRA_NAPIER, 'Napier'),
        (TIPO_CAPINEIRA_NAO_SE_APLICA, 'Não se aplica')
    )
    tipo_capineira = models.IntegerField('Tipo de Capineira', choices=tipo_capineira_choices)
    area_capineira = models.DecimalField(
        'Área da capineira (ha)', max_digits=10, decimal_places=4, blank=True, null=True
    )

    def __str__(self):
        return '{}: {}ha'.format(self.tipo_capineira_choices[self.tipo_capineira], self.area_capineira)
        return str(self.tipo_capineira)

    def save(self, *args, **kwargs):
        lote = self.lote
        lote.possui_capineira = self.CHOICE_SIM
        lote.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = ''
        verbose_name_plural = 'Sobre o Nível Tecnológico da Produção Animal'


class ProcessadoBeneficiadoManager(models.Manager):
    def get_queryset(self):
        return super(ProcessadoBeneficiadoManager, self).get_queryset().filter(classificacao=ProcessadoBeneficiado.CLASSIFICACAO_PROCESSADO_BENEFICIADO)


class ProcessadoBeneficiado(Produto):
    objects = ProcessadoBeneficiadoManager()

    def __str__(self):
        return '{} - Consumo: {}, Comércio: {}'.format(self.especificacao_choices[self.especificacao],
                                                       self.producao_consumo, self.producao_comercio)

    def save(self, *args, **kwargs):
        self.classificacao = self.CLASSIFICACAO_PROCESSADO_BENEFICIADO
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = ''
        verbose_name_plural = '36. Sobre os produtos processados ou beneficiados no estabelecimento, no último ano agrícola (agroindústria)'


class ProblemaAmbiental(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='problemasAmbientais', on_delete=models.CASCADE)

    TIPO_PROBLEMA_EROSAO = 10
    TIPO_PROBLEMA_COMPACTACAO_DO_SOLO = 20
    TIPO_PROBLEMA_CONTAMINACAO_POR_USO_DE_AGROTOXICOS_DESTINACAO_INADEQUADA_DE_EMBALAGENS = 30
    TIPO_PROBLEMA_EXPOSICAO_DE_LIXO_DE_FORMA_INADEQUADA_A_CEU_ABERTO = 40
    TIPO_PROBLEMA_QUEIMA_DE_LIXO = 50
    TIPO_PROBLEMA_DESTINACAO_INADEQUADA_DE_PILHAS_BATERIAS_LIXO_ELETRONICO = 60
    TIPO_PROBLEMA_POLUICAO_CONTAMINACAO_NASCENTE_E_OU_RIOS_CORREGOS = 70
    TIPO_PROBLEMA_ASSOREAMENTO_DE_RIO_CORREGO = 80
    TIPO_PROBLEMA_QUEIMADAS = 90
    TIPO_PROBLEMA_DESMATAMENTO = 100
    TIPO_PROBLEMA_OUTROS = 110

    tipo_problema_choices = Choices(
        (TIPO_PROBLEMA_EROSAO, 'Erosão (laminar, sulco, voçoroca)'),
        (TIPO_PROBLEMA_COMPACTACAO_DO_SOLO, 'Compactação do solo'),
        (TIPO_PROBLEMA_CONTAMINACAO_POR_USO_DE_AGROTOXICOS_DESTINACAO_INADEQUADA_DE_EMBALAGENS,
         'Contaminação por uso de  agrotóxicos/destinação inadequada de embalagens'),
        (TIPO_PROBLEMA_EXPOSICAO_DE_LIXO_DE_FORMA_INADEQUADA_A_CEU_ABERTO,
         'Exposição de lixo de forma inadequada (a céu aberto)'),
        (TIPO_PROBLEMA_QUEIMA_DE_LIXO, 'Queima de lixo'),
        (TIPO_PROBLEMA_DESTINACAO_INADEQUADA_DE_PILHAS_BATERIAS_LIXO_ELETRONICO,
         'Destinação inadequada de pilhas/baterias/lixo eletrônico'),
        (TIPO_PROBLEMA_POLUICAO_CONTAMINACAO_NASCENTE_E_OU_RIOS_CORREGOS,
         'Poluição/contaminação nascente e/ou rios/córregos'),
        (TIPO_PROBLEMA_ASSOREAMENTO_DE_RIO_CORREGO, 'Assoreamento de rio/córrego'),
        (TIPO_PROBLEMA_QUEIMADAS, 'Queimadas'),
        (TIPO_PROBLEMA_DESMATAMENTO, 'Desmatamento'),
        (TIPO_PROBLEMA_OUTROS, 'Outros')
    )
    tipo_problema = models.IntegerField('Tipo de problema', choices=tipo_problema_choices)
    outros = models.CharField('Outros (Especificar)', max_length=50, blank=True, null=True)

    def __str__(self):
        retorno = self.tipo_problema_choices[self.tipo_problema]
        if self.outros:
            retorno = retorno + ' (' + self.outros + ')'
        return retorno

    class Meta:
        verbose_name = ''
        verbose_name_plural = '40. Quais são os problemas ambientais existentes no lote?'


class PraticaConservacionista(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='praticasConservacionistas',
                             on_delete=models.CASCADE)

    TIPO_PRATICA_ADUBACAO_VERDE = 10
    TIPO_PRATICA_CURVAS_EM_NIVEL = 20
    TIPO_PRATICA_ROTACAO_CONSORCIO_DE_CULTURA = 30
    TIPO_PRATICA_ADUBACAO_ORGANICA = 40
    TIPO_PRATICA_CORDOES_DE_VEGETACAO_EM_NIVEL = 50
    TIPO_PRATICA_CONTROLE_ALTERNATIVO_DE_PRAGAS_E_DOENCAS = 60
    TIPO_PRATICA_AGROFLORESTA = 70
    TIPO_PRATICA_PLANTIOS_DE_ARVORES_PARA_PROTECAO_DE_MANACIAIS_AREAS_DEGRADADAS = 80

    tipo_pratica_choices = Choices(
        (TIPO_PRATICA_ADUBACAO_VERDE, 'Adubação verde'),
        (TIPO_PRATICA_CURVAS_EM_NIVEL, 'Curvas em nível'),
        (TIPO_PRATICA_ROTACAO_CONSORCIO_DE_CULTURA, 'Rotação/consórcio de culturas'),
        (TIPO_PRATICA_ADUBACAO_ORGANICA, 'Adubação orgânica'),
        (TIPO_PRATICA_CORDOES_DE_VEGETACAO_EM_NIVEL, 'Cordões de vegetação em nível'),
        (TIPO_PRATICA_CONTROLE_ALTERNATIVO_DE_PRAGAS_E_DOENCAS, 'Controle alternativo de pragas e doenças'),
        (TIPO_PRATICA_AGROFLORESTA, 'Agrofloresta'),
        (TIPO_PRATICA_PLANTIOS_DE_ARVORES_PARA_PROTECAO_DE_MANACIAIS_AREAS_DEGRADADAS,
         'Plantios de árvores para proteção de mananciais / áreas degradadas')
    )
    tipo_pratica = models.IntegerField('Prática Conservacionista', choices=tipo_pratica_choices)

    def __str__(self):
        return self.tipo_pratica_choices[self.tipo_pratica]

    class Meta:
        verbose_name = ''
        verbose_name_plural = '41. Quais são as práticas conservacionistas praticadas na propriedade?'


class DestinoLixoDomestico(AuditoriaAbstractModel):
    lote = models.OneToOneField(
        Lote, verbose_name='Lote', related_name='destinosLixoDomestico', on_delete=models.CASCADE,
        primary_key=True,
    )

    DESTINO_ESPALHADO_NO_LOTE = 10
    DESTINO_QUEIMA = 20
    DESTINO_ENTERRA = 30
    DESTINO_JOGA_NOS_CURSOS_DAGUA = 40
    DESTINO_RECICLA_REAPROVEITA_LIXO_INORGANICO = 50
    DESTINO_DEPOSITA_A_CEU_ABERTO_NO_LOTE = 60

    destino_choices = Choices(
        (DESTINO_ESPALHADO_NO_LOTE, 'Espalhado no lote'),
        (DESTINO_QUEIMA, 'Queima'),
        (DESTINO_ENTERRA, 'Enterra'),
        (DESTINO_JOGA_NOS_CURSOS_DAGUA, "Joga nos cursos d'água"),
        (DESTINO_RECICLA_REAPROVEITA_LIXO_INORGANICO, 'Recicla/reaproveita lixo inorgânico'),
        (DESTINO_DEPOSITA_A_CEU_ABERTO_NO_LOTE, 'Deposita a céu aberto no lote')
    )
    destino = models.IntegerField('Destino', choices=destino_choices)

    def __str__(self):
        return self.destino_choices[self.destino]

    class Meta:
        verbose_name = ''
        verbose_name_plural = '42. Qual o destino do lixo doméstico não orgânico?'


class DestinoMaterialOrganico(AuditoriaAbstractModel):
    lote = models.OneToOneField(
        Lote, verbose_name='Lote', related_name='destinosMaterialOrganico', on_delete=models.CASCADE,
        primary_key=True,
    )

    DESTINO_USO_PARA_ALIMENTACAO_DE_ANIMAIS = 10
    DESTINO_FAZ_COMPOSTAGEM = 20
    DESTINO_ENTERRA_JUNTO_COM_INORGANICO = 30
    DESTINO_DEPOSITA_A_CEU_ABERTO_NO_LOTE = 40

    destino_choices = Choices(
        (DESTINO_USO_PARA_ALIMENTACAO_DE_ANIMAIS, 'Uso para alimentação de animais'),
        (DESTINO_FAZ_COMPOSTAGEM, 'Faz compostagem'),
        (DESTINO_ENTERRA_JUNTO_COM_INORGANICO, 'Enterra junto com inorgânico'),
        (DESTINO_DEPOSITA_A_CEU_ABERTO_NO_LOTE, 'Deposita a céu aberto no lote')
    )
    destino = models.IntegerField('Destino', choices=destino_choices)

    def __str__(self):
        return self.destino_choices[self.destino]

    class Meta:
        verbose_name = ''
        verbose_name_plural = '43. Qual o destino do material orgânico?'


class LicenciamentoAmbiental(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='licenciamentosAmbientais',
                             on_delete=models.CASCADE)

    CHOICE_SIM = 1
    CHOICE_NAO = 0

    TIPO_ATIVIDADE_AGROPECUARIA = 10
    TIPO_ATIVIDADE_IRRIGACAO = 20
    TIPO_ATIVIDADE_AQUICULTURA = 30
    TIPO_ATIVIDADE_LAZER_E_TURISMO = 40
    TIPO_ATIVIDADE_OUTROS = 50

    tipo_atividade_choices = Choices(
        (TIPO_ATIVIDADE_AGROPECUARIA, 'Agropecuária'),
        (TIPO_ATIVIDADE_IRRIGACAO, 'Irrigação'),
        (TIPO_ATIVIDADE_AQUICULTURA, 'Aquicultura'),
        (TIPO_ATIVIDADE_LAZER_E_TURISMO, 'Lazer e Turismo'),
        (TIPO_ATIVIDADE_OUTROS, 'Outros')
    )
    tipo_atividade = models.IntegerField('Tipo de atividade', choices=tipo_atividade_choices)
    outros = models.CharField('Outros (Especificar)', max_length=50, blank=True, null=True)

    def __str__(self):
        retorno = self.tipo_atividade_choices[self.tipo_atividade]
        if self.outros:
            retorno = retorno + '(' + self.outros + ')'
        return retorno

    def save(self, *args, **kwargs):
        lote = self.lote
        lote.necessita_licenciamento_ambiental = self.CHOICE_SIM
        lote.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = ''
        verbose_name_plural = 'Necessita de licenciamento ambiental para alguma atividade?'


class AtendimentoSaude(AuditoriaAbstractModel):
    lote = models.OneToOneField(
        Lote, verbose_name='Lote', related_name='atendimentosSaude', on_delete=models.CASCADE,
        primary_key=True,
    )

    LOCAL_PA = 1
    LOCAL_CIDADE = 2

    local_choices = Choices(
        (LOCAL_PA, 'P.A'),
        (LOCAL_CIDADE, 'Cidade')
    )
    hospital = models.IntegerField('Hospital', choices=local_choices)
    posto_saude = models.IntegerField('Posto de saúde', choices=local_choices)
    farmacia = models.IntegerField('Farmácia', choices=local_choices)
    outros = models.IntegerField('Outros', choices=local_choices, blank=True, null=True)
    outros_especificacao = models.CharField('Outros (Especificar)', max_length=50, blank=True, null=True)

    def __str__(self):
        return 'Hospital: {}, Posto de saúde: {}, Farmácia: {}'.format(
            self.local_choices[self.hospital], self.local_choices[self.posto_saude], self.local_choices[self.farmacia]
        )

    class Meta:
        verbose_name = ''
        verbose_name_plural = '46. Onde é feito o atendimento à saúde para as famílias do assentamento?'


class ProgramaSaude(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='programasSaude', on_delete=models.CASCADE)

    PROGRAMA_SAUDE_PSF = 10
    PROGRAMA_SAUDE_AGENTES_COMUNITARIOS_DE_SAUDE = 20
    PROGRAMA_SAUDE_ATENDIMENTO_MEDICO = 30
    PROGRAMA_SAUDE_ATENDIMENTO_ODONTOLOGICO = 40
    PROGRAMA_SAUDE_CAMPANHA_DE_VACINACAO = 50
    PROGRAMA_SAUDE_SAUDE_DA_MULHER = 60

    programa_saude_choices = Choices(
        (PROGRAMA_SAUDE_PSF, 'Programa Saúde da Família - PSF'),
        (PROGRAMA_SAUDE_AGENTES_COMUNITARIOS_DE_SAUDE, 'Agentes Comunitários de Saúde'),
        (PROGRAMA_SAUDE_ATENDIMENTO_MEDICO, 'Atendimento médico'),
        (PROGRAMA_SAUDE_ATENDIMENTO_ODONTOLOGICO, 'Atendimento odontológico'),
        (PROGRAMA_SAUDE_CAMPANHA_DE_VACINACAO, 'Campanha de vacinação'),
        (PROGRAMA_SAUDE_SAUDE_DA_MULHER, 'Saúde da Mulher')
    )
    programa_saude = models.IntegerField('Programa/Tipo de atendimento à saúde', choices=programa_saude_choices)

    def __str__(self):
        return self.programa_saude_choices[self.programa_saude]

    class Meta:
        verbose_name = ''
        verbose_name_plural = '47. Quais os programas ou tipos de atendimento à saúde são disponibilizados no P.A?'


class AtividadeFisica(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='atividadesFisicas', on_delete=models.CASCADE)

    ATIVIDADE_FISICA_FUTEBOL = 10
    ATIVIDADE_FISICA_CAMINHADA_CORRIDA = 20
    ATIVIDADE_FISICA_NENHUMA_ATIVIDADE_FISICA = 30
    ATIVIDADE_FISICA_OUTROS = 40

    atividade_fisica_choices = Choices(
        (ATIVIDADE_FISICA_FUTEBOL, 'Futebol'),
        (ATIVIDADE_FISICA_CAMINHADA_CORRIDA, 'Caminhada/corrida'),
        (ATIVIDADE_FISICA_NENHUMA_ATIVIDADE_FISICA, 'Nenhuma atividade física'),
        (ATIVIDADE_FISICA_OUTROS, 'Outros')
    )
    atividade_fisica = models.IntegerField('Esporte/atividade física', choices=atividade_fisica_choices)
    outros = models.CharField('Outros (Especificar)', max_length=50, blank=True, null=True)

    def __str__(self):
        retorno = self.atividade_fisica_choices[self.atividade_fisica]
        if self.outros:
            retorno = retorno + '(' + self.outros + ')'
        return retorno

    class Meta:
        verbose_name = ''
        verbose_name_plural = '50. Quais são os esportes/atividades físicas praticados pelos familiares com maior frequência?'


class EspacoDisponivel(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='espacosDisponiveis', on_delete=models.CASCADE)

    ESPACO_DISPONIVEL_QUADRA_DE_ESPORTES = 10
    ESPACO_DISPONIVEL_CAMPO_DE_FUTEBOL = 20
    ESPACO_DISPONIVEL_SALAO_DE_FESTAS = 30
    ESPACO_DISPONIVEL_NAO_POSSUI = 40

    espaco_disponivel_choices = Choices(
        (ESPACO_DISPONIVEL_QUADRA_DE_ESPORTES, 'Quadra de esportes'),
        (ESPACO_DISPONIVEL_CAMPO_DE_FUTEBOL, 'Campo de futebol'),
        (ESPACO_DISPONIVEL_SALAO_DE_FESTAS, 'Salão de festas'),
        (ESPACO_DISPONIVEL_NAO_POSSUI, 'Não possui')
    )
    espaco_disponivel = models.IntegerField('Espaço disponível', choices=espaco_disponivel_choices)

    def __str__(self):
        return self.espaco_disponivel_choices[self.espaco_disponivel]

    class Meta:
        verbose_name = ''
        verbose_name_plural = '52. No assentamento quais são os espaços disponíveis para a prática de esporte ou para a recreação?'


class EstabelecimentoEnsino(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='estabelecimentosEnsino', on_delete=models.CASCADE)

    ESTABELECIMENTO_ENSINO_PRE_ESCOLAR_CRECHE = 10
    ESTABELECIMENTO_ENSINO_ENSINO_FUNDAMENTAL = 20
    ESTABELECIMENTO_ENSINO_EJA = 30
    ESTABELECIMENTO_ENSINO_ENSINO_MEDIO = 40
    ESTABELECIMENTO_ENSINO_ENSINO_SUPERIOR = 50
    ESTABELECIMENTO_ENSINO_ENSINO_PROFISSIONALIZANTE = 60
    ESTABELECIMENTO_ENSINO_NAO_HA_ESTABELECIMENTO_DE_ENSINO_NO_PA = 70

    estabelecimento_ensino_choices = Choices(
        (ESTABELECIMENTO_ENSINO_PRE_ESCOLAR_CRECHE, 'Pré-escolar (creche)'),
        (ESTABELECIMENTO_ENSINO_ENSINO_FUNDAMENTAL, 'Ensino Fundamental'),
        (ESTABELECIMENTO_ENSINO_EJA, 'EJA'),
        (ESTABELECIMENTO_ENSINO_ENSINO_MEDIO, 'Ensino Médio'),
        (ESTABELECIMENTO_ENSINO_ENSINO_SUPERIOR, 'Ensino Superior'),
        (ESTABELECIMENTO_ENSINO_ENSINO_PROFISSIONALIZANTE, 'Ensino Profissionalizante'),
        (ESTABELECIMENTO_ENSINO_NAO_HA_ESTABELECIMENTO_DE_ENSINO_NO_PA, 'Não há estabelecimento de ensino no PA')
    )
    estabelecimento_ensino = models.IntegerField('Estabelecimento de ensino', choices=estabelecimento_ensino_choices)

    def __str__(self):
        return self.estabelecimento_ensino_choices[self.estabelecimento_ensino]

    class Meta:
        verbose_name = ''
        verbose_name_plural = '53. Que tipo de estabelecimento de ensino está disponível no assentamento?'


class NaoPossuiDocumento(AuditoriaAbstractModel):
    lote = models.OneToOneField(
        Lote, verbose_name='Lote', related_name='nao_possui_documento', on_delete=models.CASCADE,
        primary_key=True,
    )

    certidao_nascimento = models.IntegerField('Certidão de Nascimento', blank=True, null=True)
    identidade = models.IntegerField('Identidade (RG) - a partir de 12 anos', blank=True, null=True)
    cpf = models.IntegerField('Cadastro de Pessoa Física (CPF)', blank=True, null=True)
    carteira_de_trabalho = models.IntegerField('Carteira de Trabalho (CTPS) - a partir de 14 anos', blank=True, null=True)
    certidao_de_casamento_ou_uniao_estavel = models.IntegerField('Certidão de Casamento ou União Estável', blank=True, null=True)

    def __str__(self):
        return 'Certidão de Nascimento: {}, Identidade (RG): {}, CPF: {}, Carteira de Trabalho (CTPS): {}, Certidão de Casamento ou União Estável: {}'.format(
            self.certidao_nascimento, self.identidade, self.cpf, self.carteira_de_trabalho, self.certidao_de_casamento_ou_uniao_estavel
        )

    class Meta:
        verbose_name = ''
        verbose_name_plural = '56. Com relação à documentação, quantas pessoas NÃO POSSUEM os documentos relacionados abaixo?'


# class Pessoa(AuditoriaAbstractModel):
#     nome = models.CharField('Nome', max_length=100)
#
#     PARENTESCO_CONJUGE = 1
#     PARENTESCO_TITULAR = 2
#     PARENTESCO_IRMAO_IRMA = 3
#     PARENTESCO_TIO_TIA = 4
#     PARENTESCO_PRIMO_PRIMA = 5
#     PARENTESCO_FILHO_FILHA = 6
#     PARENTESCO_CUNHADO_CUNHADA = 7
#
#     parentesco_choices = (
#         (PARENTESCO_CONJUGE, 'Cônjuge'),
#         (PARENTESCO_TITULAR, 'Titular'),
#         (PARENTESCO_CONJUGE, 'Irmão(a)'),
#         (PARENTESCO_CONJUGE, 'Tio(a)'),
#         (PARENTESCO_CONJUGE, 'Primo(a)'),
#         (PARENTESCO_CONJUGE, 'Filho(a)'),
#         (PARENTESCO_CONJUGE, 'Cunhado(a)')
#     )
#     parentesco = models.IntegerField('Parentesco', choices=parentesco_choices)
#     idade = models.IntegerField('Idade')
#
#     ESCOLARIDADE_NAO_ALFABETIZADO = 1
#     ESCOLARIDADE_1_4_ANO = 2
#     ESCOLARIDADE_5_9_ANO = 3
#     ESCOLARIDADE_FUNDAMENTAL_COMPLETO = 4
#     ESCOLARIDADE_EJA = 5
#     ESCOLARIDADE_MEDIO_INCOMPLETO = 6
#     ESCOLARIDADE_MEDIO_COMPLETO = 7
#     ESCOLARIDADE_SUPERIOR_INCOMPLETO = 8
#     ESCOLARIDADE_SUPERIOR_COMPLETO = 9
#     ESCOLARIDADE_POS_GRADUACAO_INCOMPLETA = 10
#     ESCOLARIDADE_POS_GRADUACAO_COMPLETA = 11
#
#     escolaridade_choices = (
#         (ESCOLARIDADE_NAO_ALFABETIZADO, 'Não alfabetizado'),
#         (ESCOLARIDADE_1_4_ANO, '1º ao 4º ano'),
#         (ESCOLARIDADE_5_9_ANO, '5º ao 9º ano'),
#         (ESCOLARIDADE_FUNDAMENTAL_COMPLETO, 'Fundamental completo'),
#         (ESCOLARIDADE_EJA, 'EJA - Educação de Jovens e Adultos'),
#         (ESCOLARIDADE_MEDIO_INCOMPLETO, 'Médio incompleto'),
#         (ESCOLARIDADE_MEDIO_COMPLETO, 'Médio completo'),
#         (ESCOLARIDADE_SUPERIOR_INCOMPLETO, 'Superior incompleto'),
#         (ESCOLARIDADE_SUPERIOR_COMPLETO, 'Superior completo'),
#         (ESCOLARIDADE_POS_GRADUACAO_INCOMPLETA, 'Pós Graduação incompleto'),
#         (ESCOLARIDADE_POS_GRADUACAO_COMPLETA, 'Pós Graduação completo')
#     )
#
#     CHOICE_SIM = 1
#     CHOICE_NAO = 0
#
#     sim_nao_choices = (
#         (CHOICE_SIM, 'Sim'),
#         (CHOICE_NAO, 'Não')
#     )
#     estuda = models.IntegerField('Estuda?', choices=sim_nao_choices)
#     cpf = models.CharField('CPF', max_length=11)
#
#
# class Membro(AuditoriaAbstractModel):
#     familia = models.ForeignKey('Familia', related_name="membros", on_delete=models.CASCADE)
#     pessoa = models.ForeignKey('Pessoa', related_name="membros", on_delete=models.CASCADE)
#
#
# class Familia(AuditoriaAbstractModel):
#     lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='familias', on_delete=models.CASCADE)
#     pessoas = models.ManyToManyField('Pessoa', through=Membro, through_fields=('familia', 'pessoa'),
#                                      related_name='familias')
class Familia(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='familias', on_delete=models.CASCADE)

    def __str__(self):
        return ', '.join(self.membros.values_list('nome', flat=True))

    class Meta:
        verbose_name = 'Família'
        verbose_name_plural = 'Famílias'


class Membro(AuditoriaAbstractModel):
    familia = models.ForeignKey(Familia, verbose_name='Familia', related_name='membros', on_delete=models.CASCADE)
    nome = models.CharField('Nome', max_length=100)

    PARENTESCO_TITULAR = 10
    PARENTESCO_CONJUGE = 20
    PARENTESCO_IRMAO_IRMA = 30
    PARENTESCO_TIO_TIA = 40
    PARENTESCO_PRIMO_PRIMA = 50
    PARENTESCO_FILHO_FILHA = 60
    PARENTESCO_CUNHADO_CUNHADA = 70
    PARENTESCO_GENRO_NORA = 80
    PARENTESCO_NETO_NETA = 90
    PARENTESCO_AGREGADO = 100

    parentesco_choices = Choices(
        (PARENTESCO_TITULAR, 'Titular'),
        (PARENTESCO_CONJUGE, 'Cônjuge'),
        (PARENTESCO_IRMAO_IRMA, 'Irmão(a)'),
        (PARENTESCO_TIO_TIA, 'Tio(a)'),
        (PARENTESCO_PRIMO_PRIMA, 'Primo(a)'),
        (PARENTESCO_FILHO_FILHA, 'Filho(a)'),
        (PARENTESCO_CUNHADO_CUNHADA, 'Cunhado(a)'),
        (PARENTESCO_GENRO_NORA, 'Genro/Nora'),
        (PARENTESCO_NETO_NETA, 'Neto(a)'),
        (PARENTESCO_AGREGADO, 'Agregado(a)')
    )
    parentesco = models.IntegerField('Parentesco', choices=parentesco_choices)
    idade = models.IntegerField('Idade')

    ESCOLARIDADE_NAO_ALFABETIZADO = 10
    ESCOLARIDADE_1_4_ANO = 20
    ESCOLARIDADE_5_9_ANO = 30
    ESCOLARIDADE_FUNDAMENTAL_COMPLETO = 40
    ESCOLARIDADE_EJA = 50
    ESCOLARIDADE_MEDIO_INCOMPLETO = 60
    ESCOLARIDADE_MEDIO_COMPLETO = 70
    ESCOLARIDADE_SUPERIOR_INCOMPLETO = 80
    ESCOLARIDADE_SUPERIOR_COMPLETO = 90
    ESCOLARIDADE_POS_GRADUACAO_INCOMPLETA = 100
    ESCOLARIDADE_POS_GRADUACAO_COMPLETA = 110

    escolaridade_choices = Choices(
        (ESCOLARIDADE_NAO_ALFABETIZADO, 'Não alfabetizado'),
        (ESCOLARIDADE_1_4_ANO, '1º ao 4º ano'),
        (ESCOLARIDADE_5_9_ANO, '5º ao 9º ano'),
        (ESCOLARIDADE_FUNDAMENTAL_COMPLETO, 'Fundamental completo'),
        (ESCOLARIDADE_EJA, 'EJA - Educação de Jovens e Adultos'),
        (ESCOLARIDADE_MEDIO_INCOMPLETO, 'Médio incompleto'),
        (ESCOLARIDADE_MEDIO_COMPLETO, 'Médio completo'),
        (ESCOLARIDADE_SUPERIOR_INCOMPLETO, 'Superior incompleto'),
        (ESCOLARIDADE_SUPERIOR_COMPLETO, 'Superior completo'),
        (ESCOLARIDADE_POS_GRADUACAO_INCOMPLETA, 'Pós Graduação incompleto'),
        (ESCOLARIDADE_POS_GRADUACAO_COMPLETA, 'Pós Graduação completo')
    )
    escolaridade = models.IntegerField('Escolaridade', choices=escolaridade_choices)

    CHOICE_SIM = 1
    CHOICE_NAO = 0

    sim_nao_choices = Choices(
        (CHOICE_SIM, 'Sim'),
        (CHOICE_NAO, 'Não')
    )
    estuda = models.IntegerField('Estuda?', choices=sim_nao_choices)
    cpf = models.CharField('CPF', max_length=11, unique=True, blank=True, null=True)

    TRABALHO_ANTES_DO_LOTE_SEMPRE_TRABALHOU_NO_CAMPO = 10
    TRABALHO_ANTES_DO_LOTE_TRABALHOU_PARTE_DO_TEMPO_NA_CIDADE = 20
    TRABALHO_ANTES_DO_LOTE_NUNCA_TRABALHOU_NO_CAMPO_ANTES = 30

    trabalho_antes_do_lote_choices = Choices(
        (TRABALHO_ANTES_DO_LOTE_SEMPRE_TRABALHOU_NO_CAMPO, 'Sempre trabalhou no campo'),
        (TRABALHO_ANTES_DO_LOTE_TRABALHOU_PARTE_DO_TEMPO_NA_CIDADE, 'Trabalhou parte do tempo na cidade'),
        (TRABALHO_ANTES_DO_LOTE_NUNCA_TRABALHOU_NO_CAMPO_ANTES, 'Nunca trabalhou no campo antes')
    )
    trabalho_antes_do_lote = models.IntegerField(
        'Antes de entrar no lote, trabalhava onde?', choices=trabalho_antes_do_lote_choices,
        blank=True, null=True
    )

    def __str__(self):
        return self.nome


class Contato(AuditoriaAbstractModel):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='contatos', on_delete=models.CASCADE)
    telefone = models.CharField('Telefone', max_length=12)

    def __str__(self):
        return self.telefone

    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'


class RendaTrabalhoForaLote(AuditoriaAbstractModel):
    membro = models.OneToOneField(Membro, verbose_name='Membro', related_name='renda_trabalho_fora_lote',
                                  on_delete=models.CASCADE, primary_key=True)
    quantidade_dias_ano = models.IntegerField('Quantidade de dias/ano trabalha fora do lote')
    valor = models.DecimalField('Valor da Diária (R$/dia)', max_digits=7, decimal_places=2)

    def __str__(self):
        return 'Dias/ano: {} - R$/diária: R$ {}'.format(self.quantidade_dias_ano, self.valor)

    class Meta:
        verbose_name = 'Renda de trabalho fora do lote'
        verbose_name_plural = '37. Sobre a renda de trabalho fora do lote'


class UsoFrequente(AuditoriaAbstractModel):
    membro = models.ForeignKey(Membro, verbose_name='Membro', related_name='usos_frequentes', on_delete=models.CASCADE)

    USO_FREQUENTE_BEBIDAS_ALCOOLICAS = 10
    USO_FREQUENTE_CIGARROS = 20
    USO_FREQUENTE_REMEDIOS_DE_ALTO_CUSTO = 30
    USO_FREQUENTE_OUTROS = 40

    uso_frequente_choices = Choices(
        (USO_FREQUENTE_BEBIDAS_ALCOOLICAS, 'Bebidas alcoólicas'),
        (USO_FREQUENTE_CIGARROS, 'Cigarros'),
        (USO_FREQUENTE_REMEDIOS_DE_ALTO_CUSTO, 'Remédios de alto custo'),
        (USO_FREQUENTE_OUTROS, 'Outros')
    )
    uso_frequente = models.IntegerField('Selecione', choices=uso_frequente_choices)
    outros = models.CharField('Outros (Especificar)', max_length=50, blank=True, null=True)

    def __str__(self):
        return self.uso_frequente_choices[self.uso_frequente]


    class Meta:
        verbose_name = 'Faz o uso frequente de'
        verbose_name_plural = '49. Quais os tipos de usos frequentes?'


class OpcaoEnsinoUtilizada(AuditoriaAbstractModel):
    membro = models.OneToOneField(Membro, verbose_name='Membro', related_name='opcao_ensino_utilizada',
                                  on_delete=models.CASCADE, primary_key=True)

    OPCAO_ENSINO_FREQUENTA_ESCOLA_EM_OUTRO_ASSENTAMENTO = 10
    OPCAO_ENSINO_FREQUENTA_ESCOLA_NA_CIDADE_MAIS_PROXIMA = 20
    OPCAO_ENSINO_FREQUENTA_DEIXA_DE_FREQUENTAR_A_ESCOLA = 30
    OPCAO_ENSINO_OUTROS = 40

    opcao_ensino_choices = Choices(
        (OPCAO_ENSINO_FREQUENTA_ESCOLA_EM_OUTRO_ASSENTAMENTO, 'Frequenta escola em outro assentamento'),
        (OPCAO_ENSINO_FREQUENTA_ESCOLA_NA_CIDADE_MAIS_PROXIMA, 'Frequenta escola na cidade mais próxima'),
        (OPCAO_ENSINO_FREQUENTA_DEIXA_DE_FREQUENTAR_A_ESCOLA, 'Deixa de frequentar a escola'),
        (OPCAO_ENSINO_OUTROS, 'Outros')
    )
    opcao_ensino = models.IntegerField('Selecione', choices=opcao_ensino_choices)
    outros = models.CharField('Outros (Especificar)', max_length=50, blank=True, null=True)
    distancia_percorrida = models.IntegerField('Distância até a escola (Km)')

    CHOICE_SIM = 1
    CHOICE_NAO = 0

    sim_nao_choices = Choices(
        (CHOICE_SIM, 'Sim'),
        (CHOICE_NAO, 'Não')
    )
    oferta_de_transporte = models.IntegerField('Há oferta de transporte para a escola?', choices=sim_nao_choices)

    def __str__(self):
        return self.opcao_ensino_choices[self.opcao_ensino]

    class Meta:
        verbose_name = 'Opção de ensino utilizada:'
        verbose_name_plural = '55. No caso de não haver oferta de estabelecimento de ensino apropriado no assentamento, qual a opção utilizada pelos familiares?'
