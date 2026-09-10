from django.db.models import ProtectedError
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Categoria, Producto
from .serializers import (
    CategoriaSerializer,
    ProductoPublicSerializer,
    ProductoSerializer,
)


class CategoriaListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: Lista todas las categorias registradas.
    POST: Crea una nueva categoria.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class CategoriaDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Detalle de una categoria por ID.
    PUT / PATCH: Actualizacion completa o parcial.
    DELETE: Elimina una categoria (protegida si tiene productos asociados).
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"error": "No se puede eliminar la categoría porque tiene productos asociados."},
                status=status.HTTP_400_BAD_REQUEST,
            )



class ProductoListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: Lista productos con categoria anidada (select_related).
    POST: Crea un producto recibiendo el ID de la categoria.
    """
    queryset = Producto.objects.all().select_related('categoria')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductoPublicSerializer
        return ProductoSerializer


class ProductoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Detalle de un producto con categoria anidada.
    PUT / PATCH: Actualizacion recibiendo el ID de la categoria.
    DELETE: Elimina el producto.
    """
    queryset = Producto.objects.all().select_related('categoria')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductoPublicSerializer
        return ProductoSerializer
