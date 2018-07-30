import coreapi
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework_filters.backends import DjangoFilterBackend

from rural_norte.core.models import Lote


class LoteFilterBackend(DjangoFilterBackend):
    class Meta:
        model = Lote
        fields = '__all__'

    def get_schema_fields(self, view):
        fields = super(LoteFilterBackend, self).get_schema_fields(view)
        f = [
            # coreapi.Field(name="numero", required=False, location='query', type='integer'),
        ]

        fields.extend(f)
        return fields
