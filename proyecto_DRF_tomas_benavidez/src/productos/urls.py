from django.urls import path
from . import views

urlpatterns = [
    # Categorias
    path('categorias/', views.CategoriaListCreateAPIView.as_view(), name='categoria_lista_crear'),
    path('categorias/<int:pk>/', views.CategoriaDetailAPIView.as_view(), name='categoria_detalle'),

    # Productos
    path('productos/', views.ProductoListCreateAPIView.as_view(), name='producto_lista_crear'),
    path('productos/<int:pk>/', views.ProductoDetailAPIView.as_view(), name='producto_detalle'),
]
