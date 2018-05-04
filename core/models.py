from django.db import models

class ProjetoAssentamento(models.Model):
    contrato_choices = (
        (10, '10.000/2015'),
        (11, '11.000/2015'),
        (18, '18.000/2015')
    )
    contrato = models.IntegerField('Contrato', choices=contrato_choices)
    codigo = models.CharField('Código do PA', max_length=15)
    nome = models.CharField('Nome do PA', max_length=50)
    municipio = models.CharField('Município', max_length=100)
    data_criacao = models.DateField('Data de Criação')
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.codigo, self.nome)

    class Meta:
        verbose_name = 'Projeto de Assentamento'
        verbose_name_plural = 'Projetos de Assentamento'
        ordering = ['codigo']

class Lote(models.Model):
    projeto_assentamento = models.ForeignKey(
        ProjetoAssentamento, verbose_name='PA', related_name='lotes', on_delete=models.CASCADE
    )
    codigo_sipra = models.CharField('Código SIPRA', max_length=15)
    area = models.DecimalField('Área (ha)', max_digits=10, decimal_places=4)
    numero = models.IntegerField('Lote N.º')
    entrevistador = models.CharField('Nome do Entrevistador', max_length=50)
    coordenada_x = models.CharField('Coordenada "X"', max_length=30)
    coordenada_y = models.CharField('Coordenada "Y"', max_length=30)

    sim_nao_choices = (
        (1, 'Sim'),
        (0, 'Não')
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
        'Algum dos membros da família recebe algum tipo de Benefício Social?',
        choices=sim_nao_choices
    )
    moradia_assentamento = models.IntegerField('Possui moradia no assentamento?', choices=sim_nao_choices)

    TIPO_PAREDE_ALVENARIA = 1
    TIPO_PAREDE_TABUAS_MADEIRA = 2

    tipo_parede_externa_choices = (
        (TIPO_PAREDE_ALVENARIA, 'Alvenaria'),
        (TIPO_PAREDE_TABUAS_MADEIRA, 'Tábuas / Madeira'),
        (3, 'Tapumes ou chapas de madeira'),
        (4, 'Folha de zinco'),
        (5, 'Barro ou adobe'),
        (6, 'Lona'),
        (7, 'Outros')
    )
    tipo_parede_externa = models.IntegerField(
        'Qual tipo de parede externa predominante da moradia?', choices=tipo_parede_externa_choices,
        blank=True, null=True
    )
    tipo_instalacao_eletrica_choices = (
        (1, 'Não instalada'),
        (2, 'Instalada apenas para moradia'),
        (3, 'Instalada para moradia e outros usos'),
        (4, 'Outros')
    )
    tipo_instalacao_eletrica = models.IntegerField(
        'Instalação de energia elétrica?', choices=tipo_instalacao_eletrica_choices,
        blank=True, null=True
    )
    tipo_instalacao_sanitaria_choices = (
        (1, 'Banheiro com fossa séptica'),
        (2, 'Banheiro com fossa negra'),
        (3, 'Privada / latrina'),
        (4, 'Nenhuma')
    )
    tipo_instalacao_sanitaria = models.IntegerField(
        'Qual é o tipo de instalação sanitária?', choices=tipo_instalacao_sanitaria_choices,
        blank=True, null=True
    )
    localizacao_fonte_agua_choices = (
        (1, 'Dentro do seu lote'),
        (2, 'Fora do seu lote')
    )
    localizacao_fonte_agua = models.IntegerField(
        'Onde está localizada a fonte de água que abastece sua residência?', choices=localizacao_fonte_agua_choices
    )
    abastecimento_agua_suficiente = models.IntegerField(
        'A água que abastece a residência é suficiente?', choices=sim_nao_choices
    )
    quantas_familias_utilizam_mesma_fonte_agua_choices = (
        (1, 'Nenhuma'),
        (2, 'Uma outra família, além da sua família'),
        (3, 'Mais de uma')
    )
    quantas_familias_utilizam_mesma_fonte_agua = models.IntegerField(
        'Quantas famílias (além da sua) fazem o uso da mesma fonte de água que abastece o seu lote?',
        choices=quantas_familias_utilizam_mesma_fonte_agua_choices
    )
    quantidade_familias_utilizacao_mesma_fonte_agua = models.IntegerField('Mais de uma. Quantas?', blank=True, null=True)
    agua_para_animais_plantio_choices = (
        (1, "Sim, os animais vão até um curso d'água ou represa"),
        (2, "Sim, a água é puxada de um curso d'água ou represa"),
        (3, 'Sim, temos um poço exclusivo para os animais'),
        (4, 'Sim, é a mesma água que vem para a casa'),
        (5, 'Não há água para animais'),
        (6, 'Sim, existe água para plantio(s) irrigado(s)'),
        (7, 'Não existe água para plantio(s) irrigado(s)'),
        (8, 'Outros')
    )
    agua_para_animais_plantio = models.IntegerField(
        'No lote tem água para os animais / Plantio?',choices=agua_para_animais_plantio_choices
    )
    agua_para_animais_plantio_outros = models.CharField(
        'Água para animais/plantio (Outros)', max_length=50, blank=True, null=True
    )
    regularidade_abastecimento_agua_choices = (
        (1, 'Sempre tem água'),
        (2, 'Falta água às vezes'),
        (3, 'Falta água com frequência'),
        (4, 'Nunca tem água')
    )
    regularidade_abastecimento_agua = models.IntegerField(
        'Regularidade de abastecimento de água',
        choices=regularidade_abastecimento_agua_choices
    )
    tipo_estrada_acesso_choices = (
        (1, 'Asfalto'),
        (2, 'Estrada cascalhada'),
        (3, 'Estrada de terra'),
        (4, 'Trilheiro'),
        (5, 'Inexistente')
    )
    tipo_estrada_acesso = models.IntegerField(
        'Como é o acesso ao lote?',
        choices=tipo_estrada_acesso_choices
    )
    situacao_estrada_acesso_choices = (
        (1, 'Boa'),
        (2, 'Razoável'),
        (3, 'Ruim'),
        (4, 'Péssima')
    )
    situacao_estrada_acesso = models.IntegerField(
        'Situação anual da estrada principal acesso ao lote?',
        choices=situacao_estrada_acesso_choices
    )
    situacao_cercado_lote_choices = (
        (1, 'Totalmente cercado, com divisões internas'),
        (2, 'Totalmente cercado, sem divisões internas'),
        (3, 'Parcialmente cercado'),
        (4, 'Não está cercado')
    )
    situacao_cercado_lote = models.IntegerField(
        'Como está cercado o lote?',
        choices=situacao_cercado_lote_choices
    )
    area_preservacao_permanente = models.IntegerField(
        'Existe Área de Preservação Permanente (APP) dentro do seu lote/parcela?', choices=sim_nao_choices
    )
    area_preservacao_permanente_cercada = models.IntegerField(
        'A Área de Preservação Permanente está cercada ou isolada?', choices=sim_nao_choices
    )
    necessita_licenciamento_ambiental = models.IntegerField(
        'Necessita de licenciamento ambiental de atividade?', default=0
    )
    necessita_autoriacao_exploracao_florestal_queima_controlada = models.IntegerField(
        'Necessita de autorização de exploração florestal e/ou queima controlada?', choices=sim_nao_choices
    )
    qualidade_servico_saude_choices = (
        (1, 'Ótimo'),
        (2, 'Bom'),
        (3, 'Ruim'),
        (4, 'Péssimo')
    )
    qualidade_servico_saude = models.IntegerField(
        'Como os moradores consideram o serviço de saúde no assentamento?', choices=qualidade_servico_saude_choices
    )
    frequencia_atividade_fisica_choices = (
        (1, 'Diariamente'),
        (2, 'Duas vezes por semana'),
        (3, 'Mais de duas vezes por semana'),
        (4, 'Não pratica')
    )
    frequencia_atividade_fisica = models.IntegerField(
        'Com que frequência praticam atividades físicas ou esportes?', choices=frequencia_atividade_fisica_choices
    )
    oferta_transporte_interno = models.IntegerField(
        'Para a escola do assentamento há oferta de transporte interno?', choices=sim_nao_choices
    )
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.projeto_assentamento.nome, self.codigo_sipra)

class DocumentoLote(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='documentos', on_delete=models.CASCADE)
    tipo_documento_choices = (
        (1, 'Contrato de Assentamento'),
        (2, 'Contrato de Concessão de Uso - CCU'),
        (3, 'Título Definitivo - não registrado'),
        (4, 'Título Definitivo - registrado cartório'),
        (5, 'Matrícula da Propriedade')
    )
    tipo_documento = models.IntegerField('Documento', choices=tipo_documento_choices)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return str(self.tipo_documento)

    class Meta:
        verbose_name = 'Documento do lote'
        verbose_name_plural = 'Quais documentos o lote possui?'

class BeneficioSocial(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='beneficios', on_delete=models.CASCADE)
    tipo_beneficio_choices = (
        (1, 'Aposentadoria por tempo de serviço/idade'),
        (2, 'Aposentadoria por invalidez'),
        (3, 'Auxílio maternidade'),
        (4, 'Bolsa família'),
        (5, 'Bolsa verde'),
        (6, 'Outros')
    )
    tipo_beneficio = models.IntegerField('Qual documento o lote possui?', choices=tipo_beneficio_choices)
    outros = models.CharField('Outros', max_length=30, blank=True, null=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return str(self.tipo_beneficio)

    class Meta:
        verbose_name = 'Tipo de benefício'
        verbose_name_plural = 'Quais os tipos de benefício?'

class AutoDeclaracaoEtnia(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='autoDeclaracoes', on_delete=models.CASCADE)
    tipo_declaracao_etnia_choices = (
        (1, 'Negros'),
        (2, 'Pardos'),
        (3, 'Brancos'),
        (4, 'Índios'),
        (5, 'Orientais'),
        (6, 'Outros')
    )
    tipo_declaracao_etnia = models.IntegerField('Etnia', choices=tipo_declaracao_etnia_choices)
    outros = models.CharField('Outros', max_length=30, blank=True, null=True)
    quantidade = models.IntegerField('Quantos?')
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return str(self.tipo_declaracao_etnia)

    class Meta:
        verbose_name = 'Quantos moradores se declaram?'
        verbose_name_plural = 'Quantos moradores se declaram?'

class EstruturaOrganizativa(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='estruturasOrganizativas', on_delete=models.CASCADE)
    tipo_estrutura_organizativa_choices = (
        (1, 'Associação omunitária'),
        (2, 'Cooperativas (produção, créditos, etc.)'),
        (3, 'Associação ou grupos de mulheres'),
        (4, 'Núcleos de base ligados aos movimentos'),
        (5, 'Trabalhos coletivos (ajuda mútua) "multirões"'),
        (6, 'Grupos vinculados à igreja (pastoral, etc.)'),
        (7, 'Grupos de jovens'),
        (8, 'Grupos de saúde (pastoral, farmácia viva)'),
        (9, 'Associação de pais e mestres e outros'),
        (10, 'Grupos de laser e cultura')
    )
    tipo_estrutura_organizativa = models.IntegerField('Estrutura organizativa', choices=tipo_estrutura_organizativa_choices)
    frequencia_choices = (
        (1, 'Frequente (>70%)'),
        (2, 'Regularmente (50% a 70%)'),
        (3, 'Raramente (<50%)'),
        (4, 'Não Participa'),
    )
    frequencia = models.IntegerField('Frequência', choices=frequencia_choices)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return '%s - %s' % (str(self.tipo_estrutura_organizativa), str(self.frequencia))

    class Meta:
        verbose_name = 'Estruturas organizativa interna existente'
        verbose_name_plural = 'Das estruturas organizativas internas ao assentamento diga qual existe no assentamento e de quais os membros da família participam'

class FonteAgua(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='fontesAgua', on_delete=models.CASCADE)
    fonte_agua_choices = (
        (1, 'Poço artesiano'),
        (2, 'Nascente ou vertente'),
        (3, 'Córregos ou Rios'),
        (4, 'Capitação de água da chuva'),
        (5, 'Açude / Barreiro'),
        (6, 'Poço comum'),
        (7, 'Depósito coletivo'),
        (8, 'Rede de água encanada'),
        (9, 'Outra')
    )
    fonte_agua = models.IntegerField('Fonte de água', choices=fonte_agua_choices)
    outra = models.CharField('Outra (Especificar)', max_length=30, blank=True, null=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return str(self.fonte_agua)

    class Meta:
        verbose_name = 'Abastecimento de água'
        verbose_name_plural = 'De onde vem a água que abastece a família?'

class TratamentoAgua(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='tratamentosAgua', on_delete=models.CASCADE)
    tratamento_agua_choices = (
        (1, 'Não há tratamento'),
        (2, 'Cloração'),
        (3, 'Fervura'),
        (4, 'Filtragem'),
        (5, 'Dessalinização'),
        (6, 'Outra')
    )
    tratamento_agua = models.IntegerField('Forma de tratamento', choices=tratamento_agua_choices)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return str(self.tratamento_agua)

    class Meta:
        verbose_name = 'Tratamento da água'
        verbose_name_plural = 'Qual a forma tratamento da água para consumo?'

class ConstrucaoLote(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='construcoesLote', on_delete=models.CASCADE)
    construcao_no_lote_choices = (
        (1, 'Galpão'),
        (2, 'Curral'),
        (3, 'Chiqueiro'),
        (4, 'Galinheiro'),
        (5, 'Segunda casa'),
        (6, 'Represa'),
        (7, 'Espaço para cultos religiosos'),
        (8, 'Estabelecimento comercial'),
        (9, 'Agroindústria'),
        (10, 'Outros')
    )
    construcao_no_lote = models.IntegerField('Construção', choices=construcao_no_lote_choices)
    outros = models.CharField('Outros', max_length=30, blank=True, null=True)
    quantidade = models.IntegerField('Quantidade')
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return str(self.construcao_no_lote)

    class Meta:
        verbose_name = 'Contruído no lote'
        verbose_name_plural = 'O que tem construído no lote?'

class BemProdutivo(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='bensProdutivos', on_delete=models.CASCADE)
    bem_produtivo_choices = (
        (1, 'Trator'),
        (2, 'Caminhão'),
        (3, 'Caminhonete'),
        (4, 'Arado / grade'),
        (5, 'Plantadeira / adubadeira'),
        (6, 'Pulverizador "tratorizado"'),
        (7, 'Carroça ou carro de boi'),
        (8, 'Arado de tração animal'),
        (9, 'Triturador'),
        (10, 'Resfriador de leite'),
        (11, 'Cochos'),
        (12, 'Calcariadora'),
        (13, 'Bomba (pulverizador costal)'),
        (14, 'Matraca'),
        (15, 'Brete (vacinação gado)'),
        (16, 'Roçadeira'),
        (17, 'Motossera'),
        (18, 'Outros')
    )
    bem_produtivo = models.IntegerField('Bem produtivo', choices=bem_produtivo_choices)
    outros = models.CharField('Outros', max_length=30, blank=True, null=True)
    quantidade = models.IntegerField('Quantidade')
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return str(self.bem_produtivo)

    class Meta:
        verbose_name = 'Bem produtivo'
        verbose_name_plural = 'Bens produtivos disponíveis no lote'

class AplicacaoCredito(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='aplicacoesCredito', on_delete=models.CASCADE)
    tipo_aplicacao_credito_choices = (
        (1, 'Apoio inicial (antes de 2015)'),
        (2, 'Apoio inicial I (após 2015)'),
        (3, 'Apoio inicial II (após 2015)'),
        (4, 'Fomento'),
        (5, 'Fomento Mulher'),
        (6, 'Moradia'),
        (7, 'PNHR-Minha Casa Minha Vida'),
        (8, 'Reforma Moradia'),
        (9, 'PNHR-Reforma')
    )
    tipo_aplicacao_credito = models.IntegerField('Tipo de crédito', choices=tipo_aplicacao_credito_choices)
    valor = models.DecimalField('Valor (R$)', max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return str(self.tipo_aplicacao_credito)

    class Meta:
        verbose_name = 'Aplicação do crédito no lote'
        verbose_name_plural = 'Com relação aos créditos, como está a aplicação no lote?'

class CreditoBancario(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='creditosBancarios', on_delete=models.CASCADE)
    credito_bancario_choices = (
        (1, 'Micro Crédito Produtivo (A)'),
        (2, 'A'),
        (3, 'A/C'),
        (4, 'Jovem'),
        (5, 'Mulher'),
        (6, 'Recuperação (Complementar)'),
        (7, 'Outros')
    )
    credito_bancario = models.IntegerField('Tipo de crédito', choices=credito_bancario_choices)
    outros = models.CharField('Outros', max_length=30, blank=True, null=True)
    valor = models.DecimalField('Valor (R$)', max_digits=10, decimal_places=2)
    sim_nao_choices = (
        (1, 'Sim'),
        (0, 'Não')
    )
    adimplente = models.IntegerField('Adimplente?', choices=sim_nao_choices)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return str(self.credito_bancario)

    class Meta:
        verbose_name = 'Aplicação do crédito bancário na parcela'
        verbose_name_plural = 'Com relação aos créditos bancários, como está a aplicação na parcela?'

class ProducaoVegetal(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='producoesVegetais', on_delete=models.CASCADE)
    classificacao = models.IntegerField('Classificação')
    tipo_producao_choices = (
        (1, 'Amendoim'),
        (2, 'Arroz'),
        (3, 'Batata-doce'),
        (4, 'Cana-de-Açúcar'),
        (5, 'Feijão'),
        (6, 'Mamona'),
        (7, 'Mandioca de / Farinha'),
        (8, 'Mandioca de / Mesa'),
        (9, 'Milho'),
        (10, 'Alface'),
        (11, 'Cebolinha'),
        (12, 'Couve'),
        (13, 'Coentro'),
        (14, 'Couve-flor'),
        (15, 'Rabanete'),
        (16, 'Rúcula'),
        (17, 'Salsa'),
        (18, 'Abóbora'),
        (19, 'Maxixe'),
        (20, 'Melancia'),
        (21, 'Melão'),
        (22, 'Pepino'),
        (23, 'Pimentão'),
        (24, 'Quiabo'),
        (25, 'Tomate'),
        (26, 'Abacate'),
        (27, 'Acerola'),
        (28, 'Banana'),
        (29, 'Cajú'),
        (30, 'Côco'),
        (31, 'Goiaba'),
        (32, 'Jabuticaba'),
        (33, 'Jaca'),
        (34, 'Laranja'),
        (35, 'Lima'),
        (36, 'Limão'),
        (37, 'Manga'),
        (38, 'Maracujá'),
        (39, 'Tamarindo'),
        (40, 'Tangerina'),
        (41, 'Uva'),
        (99, 'Outros')
    )
    tipo_producao = models.IntegerField('Tipo de produção', choices=tipo_producao_choices)
    tipo_producao_outros = models.CharField('Tipo de produção (Outros)', max_length=30, blank=True, null=True)
    area_plantada = models.DecimalField('Área plantada', max_digits=10, decimal_places=4)
    medida_choices = (
        (1, 'ha'),
        (2, 'm2')
    )
    medida_area_plantada = models.IntegerField('Medida da área plantada', choices=medida_choices)
    producao_consumo = models.FloatField('Produção (Consumo)', blank=True, null=True)
    producao_comercio = models.FloatField('Produção (Comércio)', blank=True, null=True)
    unidade_medida_choices = (
        (1, 'Kg'),
        (2, 'un')
    )
    producao_unidade_medida = models.IntegerField(
        'Unidade de medida da produção', choices=unidade_medida_choices, blank=True, null=True
    )
    valor = models.DecimalField('Valor (R$)', max_digits=10, decimal_places=4, blank=True, null=True)
    irrigacao_choices = (
        (1, 'Sim'),
        (2, 'Não')
    )
    irrigacao = models.IntegerField('Plantio irrigado?', choices=irrigacao_choices, blank=True, null=True)
    area_irrigada = models.DecimalField('Área irrigada', max_digits=10, decimal_places=4, blank=True, null=True)
    medida_area_irrigada = models.IntegerField('Medida da área irrigada', choices=medida_choices, blank=True, null=True)
    tipo_irrigacao_choices = (
        (1, 'Aspersão'),
        (2, 'Sulco'),
        (3, 'Gotejamento'),
        (4, 'Outros')
    )
    tipo_irrigacao = models.IntegerField('Tipo de irrigação', choices=tipo_irrigacao_choices, blank=True, null=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

class CulturaManager(models.Manager):
    def get_queryset(self):
        return super(CulturaManager, self).get_queryset().filter(classificacao=1)

class Cultura(ProducaoVegetal):
    objects = CulturaManager()

    def __str__(self):
        return '%s - %s' % ('Produção Vegetal (Cultura)', str(self.tipo_producao))

    def save(self, *args, **kwargs):
        self.classificacao = 1
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = 'Produção Vegetal - Cultura'
        verbose_name_plural = 'Produções Vegetais - Culturas'

class OlericulturaManager(models.Manager):
    def get_queryset(self):
        return super(OlericulturaManager, self).get_queryset().filter(classificacao=2)

class Olericultura(ProducaoVegetal):
    objects = OlericulturaManager()

    def __str__(self):
        return '%s - %s' % ('Produção Vegetal (Olericultura)', str(self.tipo_producao))

    def save(self, *args, **kwargs):
        self.classificacao = 2
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = 'Produção Vegetal - Olericultura'
        verbose_name_plural = 'Produções Vegetais - Olericulturas'

class FruticulturaManager(models.Manager):
    def get_queryset(self):
        return super(FruticulturaManager, self).get_queryset().filter(classificacao=3)

class Fruticultura(ProducaoVegetal):
    objects = FruticulturaManager()

    def __str__(self):
        return '%s - %s' % ('Produção Vegetal (Fruticultura)', str(self.tipo_producao))

    def save(self, *args, **kwargs):
        self.classificacao = 3
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = 'Produção Vegetal - Fruticultura'
        verbose_name_plural = 'Produções Vegetais - Fruticulturas'

class AtividadeExtrativista(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='atividadesExtrativistas', on_delete=models.CASCADE)
    especificacao_choices = (
        (1, 'Açaí(Kg)'),
        (2, 'Babaçu(Kg)'),
        (3, 'Buriti(Kg)'),
        (4, 'Cagaita(Kg)'),
        (5, 'Murici(Kg)'),
        (6, 'Pequi(Kg)'),
        (7, 'Outros')
    )
    especificacao = models.IntegerField('Especificação', choices=especificacao_choices)
    outros = models.CharField('Outros', max_length=30, blank=True, null=True)
    quantidade_frutos_ano = models.IntegerField('Quantidade Colhida / Ano - Fruto(s)')
    quantidade_palmitos_ano = models.IntegerField('Quantidade Colhida / Ano - Palmito(s)')
    valor = models.DecimalField('Valor R$/Kg', max_digits=10, decimal_places=2)

    def __str__(self):
        return '%s - %s' % ('Atividade extrativista', str(self.especificacao))

    class Meta:
        verbose_name = 'Atividade Extrativista'
        verbose_name_plural = 'Atividades Extrativistas'

class ProducaoFlorestal(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='producoesFlorestais', on_delete=models.CASCADE)
    especificacao_choices = (
        (1, 'Eucalipto(m³)'),
        (2, 'Teca(m³)'),
        (3, 'Seringueira(Kg/látex)'),
        (4, 'Seringueira(m³/Madeira)'),
        (5, 'Outros')
    )
    especificacao = models.IntegerField('Especificação', choices=especificacao_choices)
    outros = models.CharField('Outros', max_length=30, blank=True, null=True)
    quantidade_produzida_ano = models.IntegerField('Quantidade Colhida / Ano - Fruto(s)')
    area_plantada = models.DecimalField('Área plantada (ha)', max_digits=10, decimal_places=4)
    valor = models.DecimalField('R$/Unidade colhida', max_digits=10, decimal_places=2)

    def __str__(self):
        return '%s - %s' % ('Produção Florestal', str(self.especificacao))

    class Meta:
        verbose_name = 'Produção Florestal'
        verbose_name_plural = 'Produções Florestais'

class ProducaoAnimal(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='producoesAnimais', on_delete=models.CASCADE)
    classificacao = models.IntegerField('Classificação')
    tipo_criacao_choices = (
        (1, 'Gado Leiteiro'),
        (2, 'Gado de Corte')
    )
    tipo_criacao = models.IntegerField('Tipo de criação', choices=tipo_criacao_choices)
    especificacao_choices = (
        (10, 'Touros'),
        (20, 'Vacas'),
        (30, 'Novilhas(os) + de 02 anos'),
        (40, 'Novilhas(os) + de 01 ano'),
        (50, 'Bezerras(os)'),
        (60, 'Boi'),
        (70, 'Frango de corte caipira'),
        (80, 'Galinha caipira (somente frangos(as) e adultos)'),
        (90, 'Suínos'),
        (100, 'Ovinos'),
        (100, 'Equinos / Muares'),
        (120, 'Caprinos')
    )
    especificacao = models.IntegerField('Especificação', choices=especificacao_choices)
    quantidade_cabecas = models.IntegerField('Nº de Cabeça(s)')
    valor_cabeca = models.DecimalField('R$/Cabeça', max_digits=7, decimal_places=2)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

class BovinoculturaManager(models.Manager):
    def get_queryset(self):
        return super(BovinoculturaManager, self).get_queryset().filter(classificacao=1)

class Bovinocultura(ProducaoAnimal):
    objects = BovinoculturaManager()

    def __str__(self):
        return '%s - %s' % (str(self.tipo_criacao), str(self.especificacao))

    def save(self, *args, **kwargs):
        self.classificacao = 1
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = 'Produção Animal - Bovinocultura (Efetivo Atual)'
        verbose_name_plural = 'Produção Animal - Bovinocultura (Efetivo Atual)'

class OutraCriacaoManager(models.Manager):
    def get_queryset(self):
        return super(OutraCriacaoManager, self).get_queryset().filter(classificacao=2)

class OutraCriacao(ProducaoAnimal):
    objects = OutraCriacaoManager()

    def __str__(self):
        return '%s - %s' % (str(self.tipo_criacao), str(self.especificacao))

    def save(self, *args, **kwargs):
        self.classificacao = 2
        self.tipo_criacao = 3
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = 'Produção Animal - Outras Criações Animais (Efetivo Atual)'
        verbose_name_plural = 'Produção Animal - Outras Criações Animais (Efetivo Atual)'

class DescarteAnimal(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='descartesAnimais', on_delete=models.CASCADE)
    tipo_criacao = models.IntegerField('Tipo de criação')
    especificacao_choices = (
        (10, 'Touros'),
        (20, 'Vacas'),
        (30, 'Novilhas(os) + de 02 anos'),
        (40, 'Novilhas(os) + de 01 ano'),
        (50, 'Bezerras(os)'),
        (60, 'Boi')
    )
    especificacao = models.IntegerField('Especificação', choices=especificacao_choices)
    quantidade_cabecas_consumo = models.IntegerField('Nº de Cabeça(s) - Consumo')
    quantidade_cabecas_comercio = models.IntegerField('Nº de Cabeça(s) - Comércio')
    valor_cabeca = models.DecimalField('R$/Cabeça', max_digits=7, decimal_places=2)
    canal_comercializacao_choices = (
        (1, 'Venda para outro produtor'),
        (2, 'Entrega para frigorífico/açougue'),
        (3, 'Venda para agentes "atravessadores"'),
        (4, 'Outros')
    )
    canal_comercializacao = models.IntegerField('Formas/Canais de Comercialização', choices=canal_comercializacao_choices)
    canal_comercializacao_outros = models.CharField('Outros (Especificar)', max_length=30, blank=True, null=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

class BovinoculturaLeiteiraManager(models.Manager):
    def get_queryset(self):
        return super(BovinoculturaLeiteiraManager, self).get_queryset().filter(tipo_criacao=1)

class BovinoculturaLeiteira(DescarteAnimal):
    objects = BovinoculturaLeiteiraManager()

    def __str__(self):
        return '%s - %s' % (str(self.tipo_criacao), str(self.especificacao))

    def save(self, *args, **kwargs):
        self.tipo_criacao = 1
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = 'Descarte Animal - Bovinocultura Leiteira'
        verbose_name_plural = 'Descarte Animal - Bovinocultura Leiteira'

class BovinoculturaCorteManager(models.Manager):
    def get_queryset(self):
        return super(BovinoculturaCorteManager, self).get_queryset().filter(tipo_criacao=2)

class BovinoculturaCorte(DescarteAnimal):
    objects = BovinoculturaCorteManager()

    def __str__(self):
        return '%s - %s' % (str(self.tipo_criacao), str(self.especificacao))

    def save(self, *args, **kwargs):
        self.tipo_criacao = 2
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = 'Descarte Animal - Bovinocultura de Corte'
        verbose_name_plural = 'Descarte Animal - Bovinocultura de Corte'

class Produto(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='produtosOrigemAnimal', on_delete=models.CASCADE)
    classificacao = models.IntegerField('Classificação')
    especificacao_choices = (
        (1, 'Carne(Kg)'),
        (2, 'Leite(L)'),
        (3, 'Mel(Kg)'),
        (4, 'Ovos(Dz)'),
        (5, 'Peixes(Kg)'),
        (6, 'Banha(Kg)'),
        (7, 'Conservas(Un)'),
        (8, 'Doces(Un)'),
        (9, 'Farinha de Mandioca(Kg)'),
        (10, 'Linguiça(Kg)'),
        (11, 'Povilho de Mandioca(Kg)'),
        (12, 'Queijo(Kg)'),
        (13, 'Rapadura(Kg)'),
        (14, 'Outros')
    )
    especificacao = models.IntegerField('Especificação', choices=especificacao_choices)
    outros = models.CharField('Outros (Especificar)', max_length=30, blank=True, null=True)
    producao_consumo = models.IntegerField('Produção (Consumo)')
    producao_comercio = models.IntegerField('Produção (Comércio)')
    valor = models.DecimalField('Valor R$/Unidade', max_digits=7, decimal_places=2)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

class OrigemAnimalManager(models.Manager):
    def get_queryset(self):
        return super(OrigemAnimalManager, self).get_queryset().filter(classificacao=1)

class OrigemAnimal(Produto):
    objects = OrigemAnimalManager()

    def __str__(self):
        return '%s - %s' % (str(self.classificacao), str(self.especificacao))

    def save(self, *args, **kwargs):
        self.classificacao = 1
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = 'Produto de origem animal produzido'
        verbose_name_plural = 'Sobre os produtos de origem animal produzidos no último ano agrícola'

class NivelTecnologicoProducaoAnimal(models.Model):
    lote = models.OneToOneField(
        Lote, verbose_name='Lote', related_name='nivelTecnologicoProducaoAnimal', on_delete=models.CASCADE,
        primary_key=True,
    )
    sim_nao_choices = (
        (1, 'Sim'),
        (0, 'Não')
    )
    possui_capineira = models.IntegerField('Possui Capineira?', choices=sim_nao_choices)
    tipo_capineira_choices = (
        (10, 'Cana'),
        (20, 'Napier'),
        (99, 'Não se aplica')
    )
    tipo_capineira = models.IntegerField('Tipo de Capineira', choices=tipo_capineira_choices)
    area_capineira = models.DecimalField(
        'Área da capineira (ha)', max_digits=10, decimal_places=4, blank=True, null=True
    )
    possui_pastagem_rotacionada = models.IntegerField(
        'Possui Pastagem em Pastejo Rotacionado?', choices=sim_nao_choices
    )
    area_pastagem_rotacionada = models.DecimalField(
        'Área Pastejo Rotacionado (ha)', max_digits=10, decimal_places=4, blank=True, null=True
    )
    patrica_insemincacao = models.IntegerField(
        'Pratica inseminação artificial no rebanho leiteiro?', choices=sim_nao_choices
    )
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return str(self.possui_capineira)

    class Meta:
        verbose_name = 'Sobre o Nível Tecnológico da Produção Animal'
        verbose_name_plural = 'Sobre o Nível Tecnológico da Produção Animal'

class ProcessadoBeneficiadoManager(models.Manager):
    def get_queryset(self):
        return super(ProcessadoBeneficiadoManager, self).get_queryset().filter(classificacao=2)

class ProcessadoBeneficiado(Produto):
    objects = ProcessadoBeneficiadoManager()

    def __str__(self):
        return '%s - %s' % (str(self.classificacao), str(self.especificacao))

    def save(self, *args, **kwargs):
        self.classificacao = 2
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = 'Produto processado ou beneficiado'
        verbose_name_plural = 'Sobre os produtos processados ou beneficiados no estabelecimento, no último ano agrícola (agroindústria)'

class ProblemaAmbiental(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='problemasAmbientais', on_delete=models.CASCADE)
    tipo_problema_choices = (
        (1, 'Erosão (laminar, sulco, voçoroca)'),
        (2, 'Compactação do solo'),
        (3, 'Contaminação por uso de  agrotóxicos/destinação inadequada de embalagens'),
        (4, 'Exposição de lixo de forma inadequada (a céu aberto)'),
        (5, 'Queima de lixo'),
        (6, 'Destinação inadequada de pilhas/baterias/lixo eletrônico'),
        (7, 'Poluição/contaminação nascente e/ou rios/córregos'),
        (8, 'Assoreamento de rio/córrego'),
        (9, 'Queimadas'),
        (10, 'Desmatamento'),
        (11, 'Outros')
    )
    tipo_problema = models.IntegerField('Tipo de problema', choices=tipo_problema_choices)
    outros = models.CharField('Outros (Especificar)', max_length=50, blank=True, null=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return str(self.tipo_problema)

    class Meta:
        verbose_name = 'Problema ambiental'
        verbose_name_plural = 'Quais são os problemas ambientais existentes no lote?'

class PraticaConservacionista(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='praticasConservacionistas', on_delete=models.CASCADE)
    tipo_pratica_choices = (
        (10, 'Adubação verde'),
        (20, 'Curvas em nível'),
        (30, 'Rotação/consórcio de culturas'),
        (40, 'Adubação orgânica'),
        (50, 'Cordões de vegetação em nível'),
        (60, 'Controle alternativo de pragas e doenças'),
        (70, 'Agrofloresta'),
        (80, 'Plantios de árvores para proteção de mananciais / áreas degradadas')
    )
    tipo_pratica = models.IntegerField('Prática Conservacionista', choices=tipo_pratica_choices)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return str(self.tipo_pratica)

    class Meta:
        verbose_name = 'Prática conservacionista praticada'
        verbose_name_plural = 'Quais são as práticas conservacionistas praticadas na propriedade?'

class DestinoLixoDomestico(models.Model):
    lote = models.OneToOneField(
        Lote, verbose_name='Lote', related_name='destinosLixoDomestico', on_delete=models.CASCADE,
        primary_key=True,
    )
    destino_choices = (
        (10, 'Espalhado no lote'),
        (20, 'Queima'),
        (30, 'Enterra'),
        (40, "Joga nos cursos d'água"),
        (50, 'Recicla/reaproveita lixo inorgânico'),
        (60, 'Deposita a céu aberto no lote')
    )
    destino = models.IntegerField('Destino', choices=destino_choices)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return str(self.destino)

    class Meta:
        verbose_name = 'Destino do lixo doméstico não orgânico?'
        verbose_name_plural = 'Qual é o destino do lixo doméstico não orgânico?'

class DestinoMaterialOrganico(models.Model):
    lote = models.OneToOneField(
        Lote, verbose_name='Lote', related_name='destinosMaterialOrganico', on_delete=models.CASCADE,
        primary_key=True,
    )
    destino_choices = (
        (10, 'Uso para alimentação de animais'),
        (20, 'Faz compostagem'),
        (30, 'Enterra junto com inorgânico'),
        (40, 'Deposita a céu aberto no lote')
    )
    destino = models.IntegerField('Destino', choices=destino_choices)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return str(self.destino)

    class Meta:
        verbose_name = 'Destino do material orgânico?'
        verbose_name_plural = 'Qual o destino do material orgânico?'

class LicenciamentoAmbiental(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='licenciamentosAmbientais', on_delete=models.CASCADE)
    tipo_atividade_choices = (
        (1, 'Agropecuária'),
        (2, 'Irrigação'),
        (3, 'Aquicultura'),
        (4, 'Lazer e Turismo'),
        (5, 'Outros')
    )
    tipo_atividade = models.IntegerField('Tipo de atividade', choices=tipo_atividade_choices)
    outros = models.CharField('Outros (Especificar)', max_length=50, blank=True, null=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return str(self.tipo_atividade)

    def save(self, *args, **kwargs):
        lote = self.lote
        lote.necessita_licenciamento_ambiental = 1
        lote.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Licenciamento ambiental'
        verbose_name_plural = 'Necessita de licenciamento ambiental para alguma atividade?'

class AtendimentoSaude(models.Model):
    lote = models.OneToOneField(
        Lote, verbose_name='Lote', related_name='atendimentosSaude', on_delete=models.CASCADE,
        primary_key=True,
    )
    local_choices = (
        (1, 'P.A'),
        (2, 'Cidade')
    )
    hospital = models.IntegerField('Hospital', choices=local_choices)
    posto_saude = models.IntegerField('Posto de saúde', choices=local_choices)
    farmacia = models.IntegerField('Farmácia', choices=local_choices)
    outros = models.IntegerField('Outros', choices=local_choices, blank=True, null=True)
    outros_especificacao = models.CharField('Outros (Especificar)', max_length=50, blank=True, null=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return 'Hospital: %s - Posto de saúde: %s - Farmácia: %s' % (str(self.hospital), str(self.posto_saude), str(self.farmacia))

    class Meta:
        verbose_name = 'Local de atendimento à saúde'
        verbose_name_plural = 'Onde é feito o atendimento à saúde para as famílias do assentamento?'

class ProgramaSaude(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='programasSaude', on_delete=models.CASCADE)
    programa_saude_choices = (
        (10, 'Programa Saúde da Família - PSF'),
        (20, 'Agentes Comunitários de Saúde'),
        (30, 'Atendimento médico'),
        (40, 'Atendimento odontológico'),
        (50, 'Campanha de vacinação'),
        (60, 'Saúde da Mulher')
    )
    programa_saude = models.IntegerField('Programa/Tipo de atendimento à saúde', choices=programa_saude_choices)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return str(self.programa_saude)

    class Meta:
        verbose_name = 'Programa ou tipo de atendimento à saúde disponibilizado no P.A'
        verbose_name_plural = 'Quais programas ou tipos de atendimento à saúde são disponibilizados no P.A?'

class AtividadeFisica(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='atividadesFisicas', on_delete=models.CASCADE)
    atividade_fisica_choices = (
        (1, 'Futebol'),
        (2, 'Caminhada/corrida'),
        (3, 'Nenhuma atividade física'),
        (4, 'Outros')
    )
    atividade_fisica = models.IntegerField('Esporte/atividade física', choices=atividade_fisica_choices)
    outros = models.CharField('Outros (Especificar)', max_length=50, blank=True, null=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return str(self.atividade_fisica)

    class Meta:
        verbose_name = 'Esporte/atividade física praticada'
        verbose_name_plural = 'Quais são os esportes/atividades físicas praticados pelos familiares com maior frequência?'

class EspacoDisponivel(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='espacosDisponiveis', on_delete=models.CASCADE)
    espaco_disponivel_choices = (
        (1, 'Quadra de esportes'),
        (2, 'Campo de futebol'),
        (3, 'Salão de festas'),
        (4, 'Não possui')
    )
    espaco_disponivel = models.IntegerField('Espaço disponível', choices=espaco_disponivel_choices)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return str(self.espaco_disponivel)

    class Meta:
        verbose_name = 'Espaço disponível para a prática de esporte/recreação'
        verbose_name_plural = 'No assentamento quais são os espaços disponíveis para a prática de esporte ou para a recreação?'

class EstabelecimentoEnsino(models.Model):
    lote = models.ForeignKey(Lote, verbose_name='Lote', related_name='estabelecimentosEnsino', on_delete=models.CASCADE)
    estabelecimento_ensino_choices = (
        (1, 'Pré-escolar (creche)'),
        (2, 'Ensino Fundamental'),
        (3, 'EJA'),
        (4, 'Ensino Médio'),
        (5, 'Ensino Superior'),
        (6, 'Ensino Profissionalizante'),
        (7, 'Não há estabelecimento de ensino no PA')
    )
    estabelecimento_ensino = models.IntegerField('Estabelecimento de ensino', choices=estabelecimento_ensino_choices)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return str(self.estabelecimento_ensino)

    class Meta:
        verbose_name = 'Estabelecimento de ensino disponível no assentamento'
        verbose_name_plural = 'Que tipo de estabelecimento de ensino está disponível no assentamento?'