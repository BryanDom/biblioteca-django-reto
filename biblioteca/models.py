from django.db import models


class Autor(models.Model):

    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    nacionalidad = models.CharField(max_length=100, verbose_name="Nacionalidad")

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Categoria(models.Model):
    nombre_categoria = models.CharField(null=True, blank=True, max_length=100, verbose_name="Nombre Categoria")
    descripcion = models.CharField(null=True, blank=True, max_length=100, verbose_name="Descripcion Categoria")


    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["nombre_categoria"]

    def __str__(self):
        return f"{self.nombre_categoria}"


class Libro(models.Model):
    titulo = models.CharField(max_length=255, verbose_name="Título")
    nombre_categoria = models.ForeignKey(
        Categoria,
        null=True, 
        blank=True,
        on_delete=models.PROTECT,       # Se evita borrar un autor si tiene libros
        verbose_name="Categoria"
    )
    nombre_autor = models.ForeignKey(
        Autor,
        on_delete=models.PROTECT,       # Se evita borrar un autor si tiene libros
        related_name="libros",
        verbose_name="Autor",
    )
    fecha_publicacion = models.DateField(null=True, blank=True, verbose_name="Fecha de publicación")
    numero_isbn = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="ISBN",
    )
    cantidad_libros_disponibles = models.PositiveIntegerField(
        default=1,
        verbose_name="Cantidad disponible",
    )

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ["titulo"]

    def __str__(self):
        return f"{self.titulo} — {self.nombre_autor}"


class Usuario(models.Model):

    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido_paterno = models.CharField(max_length=50, default='', verbose_name="Apellido paterno")
    apellido_materno = models.CharField(max_length=50, default='', verbose_name="Apellido materno")
    correo_electronico = models.EmailField(unique=True, verbose_name="Correo electrónico")
    numero_telefono = models.CharField(max_length=20, verbose_name="Teléfono")

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["apellido_paterno", "apellido_materno", "nombre"]

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno} ({self.correo_electronico})"


class Prestamo(models.Model):

    nombre_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,       # No borrar usuario si tiene préstamos
        related_name="prestamos",
        verbose_name="Usuario",
    )
    nombre_libro = models.ForeignKey(
        Libro,
        on_delete=models.PROTECT,       # No borrar libro si está prestado
        related_name="prestamos",
        verbose_name="Libro",
    )
    fecha_inicio_prestamo = models.DateField(
        auto_now_add=True,              # Se llena automáticamente al crear
        verbose_name="Fecha de inicio",
    )
    fecha_devolucion_esperada = models.DateField(verbose_name="Fecha esperada de devolución")
    prestamo_activo = models.BooleanField(default=True, verbose_name="Préstamo activo")

    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"
        ordering = ["-fecha_inicio_prestamo"]

    def __str__(self):
        estado = "activo" if self.prestamo_activo else "devuelto"
        return f"{self.nombre_usuario} → {self.nombre_libro} ({estado})"

