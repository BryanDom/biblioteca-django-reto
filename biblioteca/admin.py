from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Autor, Libro, Usuario, Prestamo, Categoria


@admin.register(Autor)
class AutorAdmin(ImportExportModelAdmin):
    # Columnas que estan en el listado
    list_display = ("nombre", "apellido", "nacionalidad")
    # Se buscan por el nombre, apellido o nacionalidad
    search_fields = ("nombre", "apellido", "nacionalidad")
    list_filter = ("nacionalidad",)

@admin.register(Categoria)
class CategoriaAdmin(ImportExportModelAdmin):
    # Columnas que estan en el listado
    list_display = ("nombre_categoria", "descripcion")
    # Se buscan por el 
    search_fields = ("nombre_categoria", "descripcion")

@admin.register(Libro)
class LibroAdmin(ImportExportModelAdmin):
    list_display = ("titulo", "nombre_categoria", "nombre_autor", "numero_isbn", "cantidad_libros_disponibles")
    search_fields = ("titulo", "numero_isbn", "nombre_autor__nombre", "nombre_autor__apellido")
    list_filter = ("nombre_autor","nombre_categoria")
    # Aqui se puede editar la cantidad de libros disponibles
    list_editable = ("cantidad_libros_disponibles",)


@admin.register(Usuario)
class UsuarioAdmin(ImportExportModelAdmin):
    list_display = ("nombre", "apellido_paterno", "apellido_materno", "correo_electronico", "numero_telefono")
    search_fields = ("nombre", "apellido_paterno", "apellido_materno", "correo_electronico")
    list_filter = ("apellido_paterno",)


@admin.register(Prestamo)
class PrestamoAdmin(ImportExportModelAdmin):
    list_display = (
        "nombre_usuario",
        "nombre_libro",
        "fecha_inicio_prestamo",
        "fecha_devolucion_esperada",
        "prestamo_activo",
    )
    search_fields = (
        "nombre_usuario__nombre",
        "nombre_usuario__apellido_paterno",
        "nombre_libro__titulo",
    )
    list_filter = ("prestamo_activo", "fecha_inicio_prestamo")
    list_editable = ("prestamo_activo",)
    readonly_fields = ("fecha_inicio_prestamo",)
