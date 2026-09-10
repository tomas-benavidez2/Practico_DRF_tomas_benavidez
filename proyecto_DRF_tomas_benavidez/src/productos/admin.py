from django.contrib import admin
from .models import Categoria, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'activa', 'creado_en')
    list_filter = ('activa',)
    search_fields = ('nombre', 'descripcion')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria', 'precio', 'stock', 'disponible', 'creado_en')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre', 'descripcion')
