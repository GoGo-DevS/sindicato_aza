from django.shortcuts import get_object_or_404, render

from .models import Capacitacion, CategoriaCapacitacion


def capacitacion_list(request):
    categoria_slug = request.GET.get("categoria")
    categorias = CategoriaCapacitacion.objects.filter(activo=True)
    capacitaciones = Capacitacion.objects.select_related("categoria").filter(
        activo=True, categoria__activo=True
    )
    categoria_activa = None
    if categoria_slug:
        categoria_activa = get_object_or_404(CategoriaCapacitacion, slug=categoria_slug, activo=True)
        capacitaciones = capacitaciones.filter(categoria=categoria_activa)
    capacitaciones = capacitaciones.order_by("fecha", "titulo")
    return render(
        request,
        "capacitacion/capacitacion_list.html",
        {
            "capacitaciones": capacitaciones,
            "categorias": categorias,
            "categoria_activa": categoria_activa,
        },
    )


def capacitacion_detail(request, slug):
    capacitacion = get_object_or_404(
        Capacitacion.objects.select_related("categoria"),
        slug=slug,
        activo=True,
    )
    return render(
        request,
        "capacitacion/capacitacion_detail.html",
        {"capacitacion": capacitacion},
    )
