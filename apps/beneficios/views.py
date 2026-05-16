from django.views.generic import ListView

from .models import Beneficio


class BeneficioListView(ListView):
    model = Beneficio
    template_name = "beneficios/beneficio_list.html"
    context_object_name = "beneficios"
    paginate_by = 9

    def get_queryset(self):
        return (
            Beneficio.objects.select_related("categoria")
            .filter(activo=True, categoria__activo=True)
            .order_by("-destacado", "titulo")
        )
