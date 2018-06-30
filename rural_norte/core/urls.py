from django.urls import path

from rural_norte.core import views

app_name = "core"
urlpatterns = [
    path("", views.LoteListView.as_view(), name="lote-list"),
    path("login/", views.login, name="login"),
    path("contratos/", views.listar_contratos, name="listar_contratos"),
    path("contratos/<int:contrato_id>/projetos_assentamento/", views.listar_projetos_por_contrato, name="listar_projetos_por_contrato"),
    path("contratos/<int:contrato_id>/projetos_assentamento/<int:pa_id>/diagnosticos/", views.listar_diagnosticos_por_projeto_assentamento, name="listar_diagnosticos_por_projeto_assentamento"),
    path("tabela/", views.table_view, name="table_view"),
    path("tabela2/", views.Teste.as_view(), name="teste_view"),
    path("diagnostico/<int:pk>/", views.LoteDetailView.as_view(), name='lote-detail'),
    path("diagnostico/novo/<int:pa_id>/", views.novo_diagnostico, name='novo_diagnostico'),
    path("diagnostico/editar/<int:pa_id>/<int:diagnostico_id>/", views.editar_diagnostico, name='editar_diagnostico'),
    # path("diagnostico/excluir/<int:pa_id>/<int:diagnostico_id>/", views.excluir_diagnostico, name='excluir_diagnostico'),
]
