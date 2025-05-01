from django.contrib import admin
from .models import Autor, Libro, Resena

class LibroInline(admin.TabularInline):
    model = Libro
    extra = 0 

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nacionalidad')
    inlines = [LibroInline]  
    
class ResenaInline(admin.TabularInline):
    model = Resena
    extra = 0

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_publicacion')
    inlines = [ResenaInline]

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('libro', 'calificacion', 'fecha')