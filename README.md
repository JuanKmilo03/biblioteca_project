# Biblioteca

## Contributors

- Juan Camilo Banguero Melo - 1152098 - Username GitHub: juankmilo03
- Diego Alexander Granados Jaimes - 1152097 - Username GitHub: DiegoGranados15

## Biblioteca - Backend

This project contains the backend for Biblioteca, a library management web application developed with Django and SQLite. The backend provides a RESTful API that allows clients to interact with user and data.

## Installation

1. Clone this repository on your local machine:
bash
https://github.com/DIEGUS15/easycredit_API.git


2. Install the project dependencies:
bash
pip install -r requirements.txt

3. Perform database migrations:
bash
py manage.py makemigrations

bash
py manage.py migrate

4. Creating a Superuser
Once the migrations are complete, you can create a superuser with the following command:
bash
py manage.py createsuperuser

Follow the on-screen instructions to enter a username, email and password for the superuser.

5. Run the development server:
bash
py manage.py runserver

6. Enter the data you just created in the superuser and ready, you will have access to


##Captures
[![1.jpg](https://i.postimg.cc/kXFxnnpf/1.jpg)](https://postimg.cc/XpqZL03C)

[![2.jpg](https://i.postimg.cc/RVMWLwgL/2.jpg)](https://postimg.cc/PNRftvsC)

[![3.jpg](https://i.postimg.cc/66HXFR90/3.jpg)](https://postimg.cc/MXjNQnfM)

[![4.jpg](https://i.postimg.cc/wMFLQ2Jn/4.jpg)](https://postimg.cc/CnBRFjc4)

[![5.jpg](https://i.postimg.cc/vBtVGhPD/5.jpg)](https://postimg.cc/ygWdPmCz)

[![6.jpg](https://i.postimg.cc/jjr2CNnf/6.jpg)](https://postimg.cc/212rK1wj)

[![7.jpg](https://i.postimg.cc/BbyQ31GX/7.jpg)](https://postimg.cc/dZ2Km33Y)

[![8.jpg](https://i.postimg.cc/hGrDjYBF/8.jpg)](https://postimg.cc/LqJKQN5v)

[![9.jpg](https://i.postimg.cc/QtYjgWC0/9.jpg)](https://postimg.cc/Q95LhCpT)

[![10.jpg](https://i.postimg.cc/3NP7V5gG/10.jpg)](https://postimg.cc/XBcTBP1N)

[![11.jpg](https://i.postimg.cc/HsyT5ng9/11.jpg)](https://postimg.cc/3d3MQKWk)


# Proyecto Biblioteca API

API de Biblioteca desarrollada con Django REST Framework para gestionar autores, libros y reseñas.

## Características Principales

- CRUD completo para Autores, Libros y Reseñas
- Filtros y ordenamiento avanzados
- Paginación configurable
- Rutas personalizadas
- Serialización con campos calculados

## Explicación de las Funcionalidades Principales

### SerializerMethodField

El proyecto utiliza SerializerMethodField en el serializador de Libro para mostrar las reseñas más recientes sin necesidad de consultas adicionales:

python
class LibroSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='autor.nombre')
    recent_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'resumen', 'autor', 'fecha_publicacion', 'author_name', 'recent_reviews']

    def get_recent_reviews(self, obj):
        resenas = obj.resenas.order_by('-fecha')[:5]
        return ResenaSerializer(resenas, many=True).data


Esta implementación:
- Define un campo personalizado llamado recent_reviews usando SerializerMethodField()
- Implementa el método get_recent_reviews() que Django REST Framework llamará automáticamente
- Obtiene las 5 reseñas más recientes ordenándolas por fecha descendente
- Serializa estos objetos usando ResenaSerializer y los devuelve como datos estructurados

Esto permite mostrar datos relacionados de manera eficiente, controlando exactamente qué datos se incluyen y cómo se filtran, sin necesidad de crear un endpoint adicional.

### Filtros y Ordenamiento (django-filter)

El proyecto implementa filtrado y ordenamiento avanzados en el ViewSet de Libros:

python
class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
    filterset_fields = ['autor', 'fecha_publicacion']
    
    ordering_fields = ['titulo', 'fecha_publicacion']
    ordering = ['titulo'] 
    
    # Resto del código...


Esta configuración:
- Utiliza DjangoFilterBackend para filtrado y OrderingFilter para ordenamiento
- Define filterset_fields para permitir filtrado por autor y fecha_publicacion
  - Ejemplo: /api/libros/?autor=1 mostrará solo libros del autor con ID 1
- Especifica ordering_fields para permitir ordenamiento por titulo y fecha_publicacion
  - Ejemplo: /api/libros/?ordering=-fecha_publicacion ordenará los libros por fecha de publicación descendente
- Establece ordering para definir el ordenamiento predeterminado por título

El filtrado permite a los clientes de la API encontrar rápidamente recursos específicos sin tener que procesar todos los datos, mientras que el ordenamiento permite presentar los datos en el orden más útil para cada caso de uso.

### Paginación

La paginación se implementa con una clase personalizada para el ViewSet de Libros:

python
class LibroPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class LibroViewSet(viewsets.ModelViewSet):
    # Otros atributos...
    pagination_class = LibroPagination
    # Resto del código...


Esta implementación:
- Define una clase personalizada LibroPagination que hereda de PageNumberPagination
- Establece un tamaño de página predeterminado de 10 libros
- Permite modificar el tamaño de página mediante el parámetro page_size en la URL
  - Ejemplo: /api/libros/?page=2&page_size=5 mostrará la segunda página con 5 libros por página
- Limita el tamaño máximo de página a 100 para evitar sobrecarga del servidor

La paginación es esencial para mejorar el rendimiento de la API y reducir el consumo de recursos cuando se manejan grandes conjuntos de datos, permitiendo que los clientes soliciten sólo los datos que necesitan mostrar en cada momento.

### Ruta Personalizada con @action

El proyecto implementa una ruta personalizada para calcular la calificación promedio de un libro:

python
class LibroViewSet(viewsets.ModelViewSet):
    # Configuración previa...

    @action(detail=True, methods=['get'])
    def calificacion_promedio(self, request, pk=None):
        libro = self.get_object()
        promedio = libro.resenas.aggregate(promedio=Avg('calificacion'))['promedio']
        return Response({'calificacion_promedio': promedio})


Esta implementación:
- Utiliza el decorador @action de DRF para definir un endpoint personalizado
- El parámetro detail=True indica que esta acción opera sobre un libro específico (requiere un ID)
- Restringe la acción a solicitudes GET con methods=['get']
- Calcula el promedio de calificaciones utilizando una agregación del ORM de Django
- Devuelve la calificación promedio como parte de una respuesta JSON

Esta ruta puede ser accedida mediante: /api/libros/{id}/calificacion_promedio/

Las rutas personalizadas con @action permiten extender las operaciones CRUD estándar de la API RESTful con funcionalidades específicas del dominio, manteniendo una estructura organizada y coherente.

## Instalación y Configuración

1. Clonar el repositorio
2. Crear un entorno virtual: python -m venv venv
3. Activar el entorno virtual:
   - Windows: venv\Scripts\activate
   - Linux/Mac: source venv/bin/activate
4. Instalar dependencias: pip install -r requirements.txt
5. Ejecutar migraciones: python manage.py migrate
6. Iniciar servidor de desarrollo: python manage.py runserver

## Uso de la API

La API estará disponible en http://localhost:8000/api/ con los siguientes endpoints:

- /api/autores/ - CRUD de autores
- /api/libros/ - CRUD de libros con filtrado, ordenamiento y paginación
- /api/libros/{id}/calificacion_promedio/ - Calificación promedio de un libro
- /api/resenas/ - CRUD de reseñas

## Tecnologías Utilizadas

- Django
- Django REST Framework
- django-filter