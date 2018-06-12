from django import forms
from . import models

class DocumentoLoteForm(forms.ModelForm):
    class Meta:
        model = models.DocumentoLote
        fields = '__all__'

DocumentoLoteFormSet = forms.modelformset_factory(
    models.DocumentoLote,
    form=DocumentoLoteForm,
    extra=1
)

DocumentoLoteInlineFormSet = forms.inlineformset_factory(
    models.Lote,
    models.DocumentoLote,
    extra=1,
    fields=('tipo_documento',),
    formset=DocumentoLoteFormSet,
    can_delete=True,
    widgets={
        'tipo_documento': forms.Select(
            attrs={
                'class': 'form-control',
                'style': 'margin-bottom: 1em'
            }
        )
    }
)

class BeneficioSocialForm(forms.ModelForm):
    class Meta:
        model = models.BeneficioSocial
        fields = '__all__'

BeneficioSocialFormSet = forms.modelformset_factory(
    models.BeneficioSocial,
    form=BeneficioSocialForm,
    extra=1
)

BeneficioSocialInlineFormSet = forms.inlineformset_factory(
    models.Lote,
    models.BeneficioSocial,
    extra=1,
    fields=('tipo_beneficio', 'outros'),
    formset=BeneficioSocialFormSet,
    can_delete=True,
    widgets={
        'tipo_beneficio': forms.Select(
            attrs={
                'class': 'form-control',
                'style': 'margin-bottom: 1em'
            }
        ),
        'outros': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Informe o benefício'
            }
        )
    }
)

class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = models.Lote
        fields = [
            'projeto_assentamento',
            'codigo_sipra', 'data_homologacao', 'data_visita', 'area', 'numero', 'ocupante_irregular',
            'entrevistador', 'coordenada_x', 'coordenada_y', 'banda_coordenada', 'outra_familia_no_lote',
            'cad_unico', 'recebe_beneficio_social', 'moradia_assentamento', 'tipo_parede_externa',
            'tipo_instalacao_eletrica', 'tipo_instalacao_sanitaria', 'localizacao_fonte_agua',
            'abastecimento_agua_suficiente', 'quantas_familias_utilizam_mesma_fonte_agua',
            'quantidade_familias_utilizacao_mesma_fonte_agua', 'agua_para_animais_plantio',
            'agua_para_animais_plantio_outros', 'regularidade_abastecimento_agua', 'tipo_estrada_acesso',
            'situacao_estrada_acesso', 'situacao_cercado_lote', 'possui_pastagem_em_pastejo_rotacionado',
            'pratica_inseminacao_artificial_no_rebanho_leiteiro', 'area_preservacao_permanente',
            'area_preservacao_permanente_cercada', 'possui_capineira', 'area_pastejo_rotacionado',
            'necessita_licenciamento_ambiental', 'necessita_autoriacao_exploracao_florestal_queima_controlada',
            'qualidade_servico_saude', 'frequencia_atividade_fisica', 'oferta_transporte_interno'
        ]

        widgets = {
            'projeto_assentamento': forms.HiddenInput(),
            'codigo_sipra': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Informe o código'
                }
            ),
            'data_homologacao': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Informe a data'
                }
            ),
            'data_visita': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Informe a data'
                }
            ),
            'area': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Informe a área'
                }
            ),
            'numero': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Informe o número'
                }
            ),
            'ocupante_irregular': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione o status'
                }
            ),
            'entrevistador': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Inform o nome'
                }
            ),
            'coordenada_x': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Inform a coordenada'
                }
            ),
            'coordenada_y': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Inform a coordenada'
                }
            ),
            'banda_coordenada': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Inform a banda'
                }
            ),
            'outra_familia_no_lote': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'cad_unico': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'recebe_beneficio_social': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'moradia_assentamento': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'tipo_parede_externa': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'tipo_instalacao_eletrica': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'tipo_instalacao_sanitaria': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'localizacao_fonte_agua': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'abastecimento_agua_suficiente': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'quantas_familias_utilizam_mesma_fonte_agua': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'quantidade_familias_utilizacao_mesma_fonte_agua': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Informe a quantidade'
                }
            ),
            'agua_para_animais_plantio': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'agua_para_animais_plantio_outros': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Informe o nome'
                }
            ),
            'regularidade_abastecimento_agua': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'tipo_estrada_acesso': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'situacao_estrada_acesso': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'situacao_cercado_lote': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'possui_pastagem_em_pastejo_rotacionado': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'pratica_inseminacao_artificial_no_rebanho_leiteiro': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'area_preservacao_permanente': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'area_preservacao_permanente_cercada': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'possui_capineira': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'area_pastejo_rotacionado': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Informe o tamanho'
                }
            ),
            'necessita_licenciamento_ambiental': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'necessita_autoriacao_exploracao_florestal_queima_controlada': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'qualidade_servico_saude': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'frequencia_atividade_fisica': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            ),
            'oferta_transporte_interno': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione a opção'
                }
            )
        }
