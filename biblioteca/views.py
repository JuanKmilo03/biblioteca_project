from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Autor, Libro, Resena
from .serializers import AutorSerializer, LibroSerializer, ResenaSerializer
from django.db.models import Avg

class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

    def get_queryset(self):
        return Autor.objects.order_by('nombre')


class LibroPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
    filterset_fields = ['autor', 'fecha_publicacion']
    
    ordering_fields = ['titulo', 'fecha_publicacion']
    ordering = ['titulo'] 
    
    pagination_class = LibroPagination

    def get_queryset(self):
        if self.request.query_params.get('recent'):
            return Libro.objects.order_by('-fecha_publicacion')
        return Libro.objects.all()

    @action(detail=True, methods=['get'])
    def calificacion_promedio(self, request, pk=None):
        libro = self.get_object()
        promedio = libro.resenas.aggregate(promedio=Avg('calificacion'))['promedio']
        return Response({'calificacion_promedio': promedio})

class ResenaViewSet(viewsets.ModelViewSet):
    queryset = Resena.objects.all()
    serializer_class = ResenaSerializer

    def perform_create(self, serializer):
        print("Nueva reseña creada")
        serializer.save()

