from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from apps.beneficios.models import Beneficio
from apps.comunicados.models import Comunicado
from apps.contacto.models import MensajeContacto
from apps.documentos.models import Documento
from apps.siteconfig.models import SiteConfiguration

from .forms import BeneficioForm, ComunicadoForm, DocumentoForm


# ── Decorador de acceso ──────────────────────────────────────────────────────

def staff_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"/panel/login/?next={request.path}")
        if not request.user.is_staff:
            return redirect("/panel/login/")
        return view_func(request, *args, **kwargs)
    return wrapper


# ── Login / Logout ───────────────────────────────────────────────────────────

def panel_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("/panel/")

    error = None
    next_url = request.GET.get("next") or request.POST.get("next") or "/panel/"

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect(next_url)
        elif user is not None:
            error = "Su cuenta no tiene permisos para acceder al panel de administracion."
        else:
            error = "Usuario o contrasena incorrectos. Por favor intente nuevamente."

    site_config = SiteConfiguration.get_solo()
    return render(request, "panel/login.html", {
        "error": error,
        "next": next_url,
        "site_config": site_config,
    })


def panel_logout(request):
    logout(request)
    return redirect("/panel/login/")


# ── Helpers ──────────────────────────────────────────────────────────────────

def base_ctx():
    return {"mensajes_sin_leer": MensajeContacto.objects.filter(leido=False).count()}


def unique_slug(model, titulo, instance=None):
    base = slugify(titulo)
    slug, n = base, 1
    while True:
        qs = model.objects.filter(slug=slug)
        if instance and instance.pk:
            qs = qs.exclude(pk=instance.pk)
        if not qs.exists():
            return slug
        slug = f"{base}-{n}"
        n += 1


# ── Dashboard ────────────────────────────────────────────────────────────────

@staff_required
def dashboard(request):
    context = {
        **base_ctx(),
        "total_comunicados": Comunicado.objects.filter(publicado=True).count(),
        "borrador_comunicados": Comunicado.objects.filter(publicado=False).count(),
        "total_documentos": Documento.objects.count(),
        "total_beneficios": Beneficio.objects.filter(activo=True).count(),
    }
    return render(request, "panel/dashboard.html", context)


# ── Comunicados ──────────────────────────────────────────────────────────────

@staff_required
def comunicados_list(request):
    qs = Comunicado.objects.select_related("categoria").order_by("-fecha_publicacion")
    return render(request, "panel/comunicados/list.html", {**base_ctx(), "comunicados": qs})


@staff_required
def comunicados_create(request):
    form = ComunicadoForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.slug = unique_slug(Comunicado, obj.titulo)
        obj.save()
        messages.success(request, f'Comunicado "{obj.titulo}" guardado correctamente.')
        return redirect("panel:comunicados_list")
    return render(request, "panel/comunicados/form.html", {
        **base_ctx(), "form": form,
        "titulo_pagina": "Nuevo comunicado",
        "accion": "Publicar comunicado",
    })


@staff_required
def comunicados_edit(request, pk):
    obj = get_object_or_404(Comunicado, pk=pk)
    form = ComunicadoForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        comunicado = form.save(commit=False)
        if not comunicado.slug:
            comunicado.slug = unique_slug(Comunicado, comunicado.titulo, instance=comunicado)
        comunicado.save()
        messages.success(request, f'Comunicado "{comunicado.titulo}" actualizado correctamente.')
        return redirect("panel:comunicados_list")
    return render(request, "panel/comunicados/form.html", {
        **base_ctx(), "form": form, "objeto": obj,
        "titulo_pagina": f"Editar comunicado",
        "accion": "Guardar cambios",
    })


@staff_required
def comunicados_delete(request, pk):
    obj = get_object_or_404(Comunicado, pk=pk)
    if request.method == "POST":
        nombre = obj.titulo
        obj.delete()
        messages.success(request, f'Comunicado "{nombre}" eliminado.')
        return redirect("panel:comunicados_list")
    return render(request, "panel/confirm_delete.html", {
        **base_ctx(), "nombre": obj.titulo,
        "seccion": "Comunicados",
        "cancelar_url": "panel:comunicados_list",
    })


# ── Documentos ───────────────────────────────────────────────────────────────

@staff_required
def documentos_list(request):
    qs = Documento.objects.select_related("categoria").order_by("-fecha")
    return render(request, "panel/documentos/list.html", {**base_ctx(), "documentos": qs})


@staff_required
def documentos_create(request):
    form = DocumentoForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.slug = unique_slug(Documento, obj.titulo)
        obj.save()
        messages.success(request, f'Documento "{obj.titulo}" subido correctamente.')
        return redirect("panel:documentos_list")
    return render(request, "panel/documentos/form.html", {
        **base_ctx(), "form": form,
        "titulo_pagina": "Subir documento",
        "accion": "Subir documento",
    })


@staff_required
def documentos_edit(request, pk):
    obj = get_object_or_404(Documento, pk=pk)
    form = DocumentoForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        doc = form.save(commit=False)
        if not doc.slug:
            doc.slug = unique_slug(Documento, doc.titulo, instance=doc)
        doc.save()
        messages.success(request, f'Documento "{doc.titulo}" actualizado correctamente.')
        return redirect("panel:documentos_list")
    return render(request, "panel/documentos/form.html", {
        **base_ctx(), "form": form, "objeto": obj,
        "titulo_pagina": "Editar documento",
        "accion": "Guardar cambios",
    })


@staff_required
def documentos_delete(request, pk):
    obj = get_object_or_404(Documento, pk=pk)
    if request.method == "POST":
        nombre = obj.titulo
        obj.delete()
        messages.success(request, f'Documento "{nombre}" eliminado.')
        return redirect("panel:documentos_list")
    return render(request, "panel/confirm_delete.html", {
        **base_ctx(), "nombre": obj.titulo,
        "seccion": "Documentos",
        "cancelar_url": "panel:documentos_list",
    })


# ── Beneficios ───────────────────────────────────────────────────────────────

@staff_required
def beneficios_list(request):
    qs = Beneficio.objects.select_related("categoria").order_by("activo", "-vigencia")
    return render(request, "panel/beneficios/list.html", {**base_ctx(), "beneficios": qs})


@staff_required
def beneficios_create(request):
    form = BeneficioForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.slug = unique_slug(Beneficio, obj.titulo)
        obj.save()
        messages.success(request, f'Beneficio "{obj.titulo}" creado correctamente.')
        return redirect("panel:beneficios_list")
    return render(request, "panel/beneficios/form.html", {
        **base_ctx(), "form": form,
        "titulo_pagina": "Nuevo beneficio",
        "accion": "Guardar beneficio",
    })


@staff_required
def beneficios_edit(request, pk):
    obj = get_object_or_404(Beneficio, pk=pk)
    form = BeneficioForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        beneficio = form.save(commit=False)
        if not beneficio.slug:
            beneficio.slug = unique_slug(Beneficio, beneficio.titulo, instance=beneficio)
        beneficio.save()
        messages.success(request, f'Beneficio "{beneficio.titulo}" actualizado correctamente.')
        return redirect("panel:beneficios_list")
    return render(request, "panel/beneficios/form.html", {
        **base_ctx(), "form": form, "objeto": obj,
        "titulo_pagina": "Editar beneficio",
        "accion": "Guardar cambios",
    })


@staff_required
def beneficios_delete(request, pk):
    obj = get_object_or_404(Beneficio, pk=pk)
    if request.method == "POST":
        nombre = obj.titulo
        obj.delete()
        messages.success(request, f'Beneficio "{nombre}" eliminado.')
        return redirect("panel:beneficios_list")
    return render(request, "panel/confirm_delete.html", {
        **base_ctx(), "nombre": obj.titulo,
        "seccion": "Beneficios",
        "cancelar_url": "panel:beneficios_list",
    })


# ── Mensajes ─────────────────────────────────────────────────────────────────

@staff_required
def mensajes_list(request):
    qs = MensajeContacto.objects.order_by("leido", "-created_at")
    return render(request, "panel/mensajes/list.html", {**base_ctx(), "mensajes": qs})


@staff_required
def mensaje_detail(request, pk):
    mensaje = get_object_or_404(MensajeContacto, pk=pk)
    if not mensaje.leido:
        mensaje.leido = True
        mensaje.save(update_fields=["leido"])
    if request.method == "POST":
        mensaje.respondido = True
        mensaje.save(update_fields=["respondido"])
        messages.success(request, "Mensaje marcado como respondido.")
        return redirect("panel:mensajes_list")
    return render(request, "panel/mensajes/detail.html", {**base_ctx(), "mensaje": mensaje})
