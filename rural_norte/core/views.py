from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, DetailView

from rural_norte.core import models

class LoteListView(ListView):

    model = models.Lote

class LoteDetailView(DetailView):

    model = models.Lote

def listar_contratos(request):
    contratos = models.Contrato.objects.all()
    template_name = 'core/listar_contratos.html'
    context = {
        'contratos': contratos
    }
    return render(request, template_name, context)
