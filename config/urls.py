from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from biblioteca.views import (
    AutorViewSet, LibroViewSet, UsuarioViewSet, PrestamoViewSet,
    lista_prestamo, crear_prestamo, editar_prestamo, eliminar_prestamo,
)

# Se hace un Router de DRF para generar automáticamente todas las URLs de CRUD de cada modelo.
router = DefaultRouter()
router.register(r"autores", AutorViewSet, basename="autor")
router.register(r"libros", LibroViewSet, basename="libro")
router.register(r"usuarios", UsuarioViewSet, basename="usuario")
router.register(r"prestamos", PrestamoViewSet, basename="prestamo")

# Se hace un Swagger para que en /api/redoc o /api/docs se genere la documentación de la API.
schema_view = get_schema_view(
    openapi.Info(
        title="API (documentación de la API del sistema de gestión de biblioteca)", # sut itulo
        default_version="v1", # la version de la api que estamosm anjeando por ejemplo
        description="Documentacion de la API del sistema de gestión de biblioteca donde se gestionan autores, libros, usuarios y prestamos", 
        contact=openapi.Contact(email="brayandom1604@gmail.com"), #el contacto de la api que se muestra en la documentacion 
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    # Para el panel de administración de Django.
    path("admin/", admin.site.urls),

    # Esto para generar el Token.
    path("api/token/", obtain_auth_token, name="api-token"),

    # Aquí se obtienen todas las rutas CRUD de los modelos.
    path("api/", include(router.urls)),

    # Aquí se obtiene la documentación de la API en formato Swagger
    path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),

    # Aquí se obtiene la documentación de la API en formato ReDoc.
    path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-ui"),

    #interfaces para prestamos.
    path("", lista_prestamo, name="lista_prestamo"),
    path("prestamos/crear/", crear_prestamo, name="crear_prestamo"),
    path("prestamos/<int:pk>/editar/", editar_prestamo, name="editar_prestamo"),
    path("prestamos/<int:pk>/eliminar/", eliminar_prestamo, name="eliminar_prestamo"),
]
