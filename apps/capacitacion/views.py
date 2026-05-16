from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import RecursoAyuda


@login_required
def ayuda_list(request):
    recursos = RecursoAyuda.objects.filter(activo=True)

    context = {
        "videos":      recursos.filter(tipo="video"),
        "pdfs":        recursos.filter(tipo="pdf"),
        "guias":       recursos.filter(tipo="guia"),
        "presenciales": recursos.filter(tipo="presencial"),
        "total":       recursos.count(),
    }
    return render(request, "capacitacion/ayuda_list.html", context)
