from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Autor, Libro, Usuario, Prestamo
from .serializers import AutorSerializer, LibroSerializer, UsuarioSerializer, PrestamoSerializer
from .forms import PrestamoForm



# Vistas para la API REST

class AutorViewSet(viewsets.ModelViewSet):
    # CRUD  para el modelo de los autores de la biblioteca donde si o si se requiere autenticación por el Token.

    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [IsAuthenticated]


class LibroViewSet(viewsets.ModelViewSet):
    # CRUD para el modelo de libros de la biblioteca donde se requiere autenticación por el Token.

    queryset = Libro.objects.select_related("nombre_autor").all()
    serializer_class = LibroSerializer
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



# Vistas para las páginas web de Préstamos utilizando Django Templates

def lista_prestamo(request):
    prestamos = Prestamo.objects.select_related("nombre_usuario", "nombre_libro").all()
    return render(request, "prestamos/lista.html", {"prestamos": prestamos})


def crear_prestamo(request):
    if request.method == "POST":
        formulario = PrestamoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Se registro el préstamo correctamente")
            return redirect("lista_prestamo") #volvemos a la lista de los prestamos
    else:
        formulario = PrestamoForm()

    return render(request, "prestamos/formulario.html", {"form": formulario})


def editar_prestamo(request, pk):
    # recibimos la llave priamria del prestamo a editar del registro.
    prestamo = get_object_or_404(Prestamo, pk=pk)

    if request.method == "POST":
        formulario = PrestamoForm(request.POST, instance=prestamo)
        if formulario.is_valid():
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
        prestamo.delete()
        messages.success(request, "Se elimino el prestamo correctamente")
        return redirect("lista_prestamo")

    return render(request, "prestamos/confirmar_eliminar.html", {"prestamo": prestamo})
