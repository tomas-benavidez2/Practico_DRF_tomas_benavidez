from django.db.models import ProtectedError
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Categoria, Producto
from .serializers import (
    CategoriaSerializer,
    ProductoPublicSerializer,
    ProductoSerializer,
)


class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para Categorias.
    Provee automaticamente las acciones:
    - GET /api/categorias/ -> list
    - GET /api/categorias/<id>/ -> retrieve
    Acceso publico sin autenticacion requerida (AllowAny).
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny]


class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet con CRUD completo para Productos.
    Provee las acciones:
    - GET /api/productos/ -> list
    - POST /api/productos/ -> create (requiere autenticacion)
    - GET /api/productos/<id>/ -> retrieve
    - PUT /api/productos/<id>/ -> update (requiere autenticacion)
    - PATCH /api/productos/<id>/ -> partial_update (requiere autenticacion)
    - DELETE /api/productos/<id>/ -> destroy (requiere autenticacion)
    - GET /api/productos/disponibles/ -> accion personalizada (AllowAny)
    """
    queryset = Producto.objects.all().select_related('categoria')

    def get_serializer_class(self):
        """
        Usa ProductoSerializer en mutaciones (create, update, partial_update, POST, PUT, PATCH)
        y ProductoPublicSerializer (categoria anidada) en lecturas (GET, list, retrieve, disponibles).
        """
        if (
            self.action in ['create', 'update', 'partial_update']
            or (self.request and self.request.method not in permissions.SAFE_METHODS)
        ):
            return ProductoSerializer
        return ProductoPublicSerializer

    def get_permissions(self):
        """
        Define permisos dinámicos según la acción y el método HTTP:
        - Acciones y métodos de modificación (create, update, partial_update, destroy o métodos no seguros): IsAuthenticated.
        - Acciones y métodos de consulta pública (list, retrieve, disponibles o métodos seguros): AllowAny.
        """
        if (
            self.action in ['create', 'update', 'partial_update', 'destroy']
            or (self.request and self.request.method not in permissions.SAFE_METHODS)
        ):
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], url_path='disponibles')
    def disponibles(self, request):
        """
        GET /api/productos/disponibles/
        Retorna la lista de productos cuyo campo disponible es True.
        """
        queryset = self.filter_queryset(self.get_queryset().filter(disponible=True))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Elimina el producto asegurando manejo ante posibles ProtectedError.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"error": "No se puede eliminar el producto porque tiene registros relacionados protegidos."},
                status=status.HTTP_400_BAD_REQUEST,
            )
