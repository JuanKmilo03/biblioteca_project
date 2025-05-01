from biblioteca.models import Autor, Libro, Resena

Resena.objects.all().delete()
Libro.objects.all().delete()
Autor.objects.all().delete()

autor1 = Autor.objects.create(nombre="Gabriel Garcia Marquez", nacionalidad="Colombiana")
autor2 = Autor.objects.create(nombre="Isabel Allende", nacionalidad="Chilena")

libro1 = Libro.objects.create(titulo="Cien anios de soledad", autor=autor1, fecha_publicacion="1967-06-05", resumen="Novela emblematica del realismo magico.")
libro2 = Libro.objects.create(titulo="La casa de los espiritus", autor=autor2, fecha_publicacion="1982-01-01", resumen="Una historia familiar con elementos sobrenaturales.")

Resena.objects.create(libro=libro1, texto="Excelente obra literaria", calificacion=5)
Resena.objects.create(libro=libro2, texto="Muy recomendable", calificacion=4)