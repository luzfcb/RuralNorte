from django.utils import timezone
from django.views.generic import ListView, DetailView

from .models import Lote

class LoteListView(ListView):

    model = Lote

class LoteDetailView(DetailView):

    model = Lote
