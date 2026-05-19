from rest_framework import serializers
from .models import Autor, Libro, Usuario, Prestamo, Categoria


class AutorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Autor
        fields = "__all__"

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"


class LibroSerializer(serializers.ModelSerializer):

    # En las respuestas, se mostrará el nombre completo del autor donde es de lectura este campo que se agrega
    autor_nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Libro
        fields = "__all__"

    def get_autor_nombre_completo(self, obj):
        return str(obj.nombre_autor)


class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = "__all__"


class PrestamoSerializer(serializers.ModelSerializer):

    # Muestran informacion legible en las respuestas GET de prestamos 
    usuario_nombre = serializers.SerializerMethodField()
    libro_titulo = serializers.SerializerMethodField()

    class Meta:
        model = Prestamo
        fields = "__all__"

    def get_usuario_nombre(self, obj):
        return str(obj.nombre_usuario)

    def get_libro_titulo(self, obj):
        return str(obj.nombre_libro)

    def validate(self, datos):
        from datetime import date

        # Valida que la fecha de devolución sea posterior a la fecha actual
        fecha_devolucion = datos.get("fecha_devolucion_esperada")
        if fecha_devolucion and fecha_devolucion < date.today():
            raise serializers.ValidationError(
                {"fecha_devolucion_esperada": "La fecha de devolución no puede ser en el pasado."}
            )

        return datos
