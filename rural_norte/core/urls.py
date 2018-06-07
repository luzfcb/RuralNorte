from django.urls import path

from rural_norte.core import views

app_name = "core"
urlpatterns = [
    path("", views.LoteListView.as_view(), name="lote-list"),
    path("contratos/", views.listar_contratos, name="listar_contratos"),
    path("contratos/<int:contrato_id>/projetos_assentamento/", views.listar_projetos_por_contrato, name="listar_projetos_por_contrato"),
    path("contratos/<int:contrato_id>/projetos_assentamento/<int:pa_id>/diagnosticos/", views.listar_diagnosticos_por_projeto_assentamento, name="listar_diagnosticos_por_projeto_assentamento"),
    path("tabela/", views.table_view, name="table_view"),
    path("tabela2/", views.Teste.as_view(), name="teste_view"),
    path('<int:pk>/', views.LoteDetailView.as_view(), name='lote-detail'),
]
