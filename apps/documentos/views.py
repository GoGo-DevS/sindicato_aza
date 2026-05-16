from django.views.generic import ListView

from .models import CategoriaDocumento, Documento


class DocumentoListView(ListView):
    model = Documento
    template_name = "documentos/documento_list.html"
    context_object_name = "documentos"
    paginate_by = 12

    def get_queryset(self):
        queryset = (
            Documento.objects.select_related("categoria")
            .filter(publico=True, categoria__activo=True)
            .order_by("-destacado", "-fecha", "titulo")
        )
        self.categoria_actual = None
        categoria_slug = self.request.GET.get("categoria")
        if categoria_slug:
            queryset = queryset.filter(categoria__slug=categoria_slug)
            self.categoria_actual = CategoriaDocumento.objects.filter(
                slug=categoria_slug,
                activo=True,
            ).first()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias"] = CategoriaDocumento.objects.filter(activo=True)
        context["categoria_actual"] = self.categoria_actual
        return context
