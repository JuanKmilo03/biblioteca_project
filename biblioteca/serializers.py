from rest_framework import serializers
from .models import Autor, Libro, Resena

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = 'id', 'nombre', 'nacionalidad'

class ResenaSerializer(serializers.ModelSerializer):
    libro_titulo = serializers.ReadOnlyField(source='libro.titulo')
    class Meta:
        model = Resena
        fields = ['id', 'libro', 'libro_titulo', 'texto', 'calificacion', 'fecha']

class LibroSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='autor.nombre')
    recent_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'resumen', 'autor', 'fecha_publicacion', 'author_name', 'recent_reviews']

    def get_recent_reviews(self, obj):
        resenas = obj.resenas.order_by('-fecha')[:5]
        return ResenaSerializer(resenas, many=True).data
