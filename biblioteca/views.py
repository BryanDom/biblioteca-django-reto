from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Autor, Libro, Usuario, Prestamo, Categoria
from .serializers import AutorSerializer, LibroSerializer, UsuarioSerializer, PrestamoSerializer, CategoriaSerializer
from .forms import PrestamoForm



# Vistas para la API REST

class AutorViewSet(viewsets.ModelViewSet):
    # CRUD  para el modelo de los autores de la biblioteca donde si o si se requiere autenticación por el Token.

    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [IsAuthenticated]

class CategoriaViewSet(viewsets.ModelViewSet):
    # CRUD para el modelo de libros de la biblioteca donde se requiere autenticación por el Token.

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]


class LibroViewSet(viewsets.ModelViewSet):
    # CRUD para el modelo de libros de la biblioteca donde se requiere autenticación por el Token.

    queryset = Libro.objects.select_related("nombre_autor").all()
    serializer_class = LibroSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre_categoria__nombre_categoria']
    permission_classes = [IsAuthenticated]


class UsuarioViewSet(viewsets.ModelViewSet):
    # CRUD para el modelo de usuarios de la biblioteca donde se requiere autenticación por el Token.

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]


class PrestamoViewSet(viewsets.ModelViewSet):
    # CRUD para el modelo de prestamos de la biblioteca donde se requiere autenticación por el Token.

    queryset = Prestamo.objects.select_related("nombre_usuario", "nombre_libro").all()
    serializer_class = PrestamoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """POST /api/prestamos/ → Crea préstamo y resta 1 al stock del libro."""
        libro = serializer.validated_data["nombre_libro"]

        if libro.cantidad_libros_disponibles <= 0:
            raise ValidationError({"nombre_libro": f"No hay libros disponibles de '{libro.titulo}'."})

        # Guardamos el préstamo siempre activo
        prestamo = serializer.save(prestamo_activo=True)

        # Restamos el stock
        libro.cantidad_libros_disponibles -= 1
        libro.save(update_fields=["cantidad_libros_disponibles"])

    def perform_update(self, serializer):
        """PUT/PATCH /api/prestamos/{id}/ → Maneja el stock según el cambio de estado."""
        prestamo_anterior = self.get_object()  # Estado ANTES del update
        libro = prestamo_anterior.nombre_libro

        nuevo_estado = serializer.validated_data.get("prestamo_activo", prestamo_anterior.prestamo_activo)

        # Caso: reactivar un préstamo devuelto (False → True) → restar stock
        if prestamo_anterior.prestamo_activo is False and nuevo_estado is True:
            if libro.cantidad_libros_disponibles <= 0:
                raise ValidationError({"prestamo_activo": f"No se puede reactivar: '{libro.titulo}' no tiene stock disponible."})
            serializer.save()
            libro.cantidad_libros_disponibles -= 1
            libro.save(update_fields=["cantidad_libros_disponibles"])

        # Caso: devolver un libro (True → False) → sumar stock
        elif prestamo_anterior.prestamo_activo is True and nuevo_estado is False:
            serializer.save()
            libro.cantidad_libros_disponibles += 1
            libro.save(update_fields=["cantidad_libros_disponibles"])

        # Caso: sin cambio en el estado → solo guarda
        else:
            serializer.save()


# ──────────────────────────────────────────────────────────
# Vistas para Django Templates (interfaz web)
# ──────────────────────────────────────────────────────────

def lista_prestamo(request):
    from django.core.paginator import Paginator

    todos_los_prestamos = Prestamo.objects.select_related("nombre_usuario", "nombre_libro").all()

    paginator = Paginator(todos_los_prestamos, 5)          # 5 préstamos por página
    numero_pagina = request.GET.get("page", 1)             # ?page=1 por defecto
    prestamos = paginator.get_page(numero_pagina)          # página actual

    return render(request, "prestamos/lista.html", {"prestamos": prestamos})


def crear_prestamo(request):
    if request.method == "POST":
        formulario = PrestamoForm(request.POST)
        if formulario.is_valid():
            libro = formulario.cleaned_data["nombre_libro"]

            if libro.cantidad_libros_disponibles <= 0:
                messages.error(request, f"No hay libros disponibles de '{libro.titulo}'.")
                return render(request, "prestamos/formulario.html", {"form": formulario})

            # Guardamos el préstamo siempre activo
            prestamo = formulario.save(commit=False)
            prestamo.prestamo_activo = True
            prestamo.save()

            # Restamos el stock
            libro.cantidad_libros_disponibles -= 1
            libro.save(update_fields=["cantidad_libros_disponibles"])

            messages.success(request, "Préstamo registrado correctamente.")
            return redirect("lista_prestamo")
    else:
        formulario = PrestamoForm()

    return render(request, "prestamos/formulario.html", {"form": formulario})


def editar_prestamo(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)

    if request.method == "POST":
        formulario = PrestamoForm(request.POST, instance=prestamo)
        if formulario.is_valid():
            estado_anterior = prestamo.prestamo_activo
            nuevo_estado = formulario.cleaned_data["prestamo_activo"]
            libro = formulario.cleaned_data["nombre_libro"]

            # Caso: reactivar préstamo devuelto (False → True) → restar stock
            if estado_anterior is False and nuevo_estado is True:
                if libro.cantidad_libros_disponibles <= 0:
                    messages.error(request, f"No se puede reactivar: '{libro.titulo}' no tiene stock disponible.")
                    return render(request, "prestamos/formulario.html", {"form": formulario})
                formulario.save()
                libro.cantidad_libros_disponibles -= 1
                libro.save(update_fields=["cantidad_libros_disponibles"])

            # Caso: devolver libro (True → False) → sumar stock
            elif estado_anterior is True and nuevo_estado is False:
                formulario.save()
                libro.cantidad_libros_disponibles += 1
                libro.save(update_fields=["cantidad_libros_disponibles"])

            # Caso: sin cambio de estado → solo guarda
            else:
                formulario.save()

            messages.success(request, "Préstamo actualizado correctamente.")
            return redirect("lista_prestamo")
    else:
        formulario = PrestamoForm(instance=prestamo)

    return render(request, "prestamos/formulario.html", {"form": formulario})


def eliminar_prestamo(request, pk):
    # recibimos la llave priamria del prestamo a eliminar del registro.
    prestamo = get_object_or_404(Prestamo, pk=pk)

    if request.method == "POST":
        # Si el préstamo está activo al eliminarlo, devolvemos el stock
        if prestamo.prestamo_activo:
            libro = prestamo.nombre_libro
            libro.cantidad_libros_disponibles += 1
            libro.save(update_fields=["cantidad_libros_disponibles"])

        prestamo.delete()
        messages.success(request, "Préstamo eliminado correctamente.")
        return redirect("lista_prestamo")

    return render(request, "prestamos/confirmar_eliminar.html", {"prestamo": prestamo})
