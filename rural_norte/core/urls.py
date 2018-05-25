from django.urls import path

from .views import LoteListView, LoteDetailView

app_name = "core"
urlpatterns = [
    path("", LoteListView.as_view(), name="lote-list"),
    # path('detalhes/(?P<pk>\d+)/$', LoteDetailView.as_view(), name='lote-detail'),
    path('<int:pk>/', LoteDetailView.as_view(), name='lote-detail'),
]
