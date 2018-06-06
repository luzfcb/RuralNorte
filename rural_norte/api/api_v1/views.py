from django.db.models import Q

from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet

from rural_norte.core.models import Lote

from .paginators import StandardResultsSetPagination
from .serializers import LoteHyperlinkedModelSerializer, LoteModelSerializer
from .filters import LoteFilterBackend


class LoteViewSet(ReadOnlyModelViewSet):
    filter_backends = (
        # django_filters.rest_framework.DjangoFilterBackend,
        LoteFilterBackend,
    )
    queryset = Lote.objects.order_by('-cadastrado_em')
    # serializer_class = LoteHyperlinkedModelSerializer
    serializer_class = LoteModelSerializer
    permission_classes = (
        permissions.DjangoModelPermissions,
    )
    pagination_class = StandardResultsSetPagination
    # lookup_field = 'numero'
    # lookup_url_kwarg = 'numero'

    def get_queryset(self):
        queryset = super(LoteViewSet, self).get_queryset()
        q = Q()

        numero = self.request.query_params.get('numero', None) or None
        pessoa_parte = self.request.query_params.get('partes__pessoa', None) or None

        return queryset.filter(q)

    def filter_queryset(self, queryset):
        # queryset = queryset.only('pk', 'numero', 'inicial')
        queryset = queryset
        return super(LoteViewSet, self).filter_queryset(queryset)
