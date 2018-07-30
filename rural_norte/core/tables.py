from django_tables2 import tables

from . import models
from django_tables2.columns import Column

class LoteTable(tables.Table):
    teste = Column()

    def render_teste(self, record):
        return '<%s>' % record

    class Meta:
        model = models.Lote
        fields = ['cadastrado_por', 'entrevistador']
        template_name = 'django_tables2/bootstrap.html'
