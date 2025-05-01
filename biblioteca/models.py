from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

def validar_nombre_no_vacio(value):
    if not value.strip():
        raise ValidationError('El nombre no puede estar vacío o solo tener espacios.')

def validar_resumen_minimo(value):
    if len(value) < 30:
        raise ValidationError('El resumen debe tener al menos 30 caracteres.')

class Autor(models.Model):
    nombre = models.CharField(max_length=100, validators=[validar_nombre_no_vacio])
    nacionalidad = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    resumen = models.TextField(validators=[validar_resumen_minimo])
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    fecha_publicacion = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Resena(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='resenas')
    texto = models.TextField()
    calificacion = models.FloatField(
        validators=[
            MinValueValidator(0.0), MaxValueValidator(5.0)
        ]
    )
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.libro.titulo} : {self.calificacion}/5"
