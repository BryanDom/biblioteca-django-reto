from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Autor, Libro, Usuario, Prestamo
from .serializers import AutorSerializer, LibroSerializer, UsuarioSerializer, PrestamoSerializer


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
