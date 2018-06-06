from django.urls import path

from rural_norte.core import views

app_name = "core"
urlpatterns = [
    path("", views.LoteListView.as_view(), name="lote-list"),
    path("contratos/", views.listar_contratos, name="listar_contratos"),
    path("tabela/", views.table_view, name="table_view"),
    path("tabela2/", views.Teste.as_view(), name="teste_view"),
    # path('detalhes/(?P<pk>\d+)/$', LoteDetailView.as_view(), name='lote-detail'),
    path('<int:pk>/', views.LoteDetailView.as_view(), name='lote-detail'),
]
