from django_tables2 import tables

from . import models

class LoteTable(tables.Table):
    class Meta:
        model = models.Lote
        template_name = 'django_tables2/bootstrap.html'
