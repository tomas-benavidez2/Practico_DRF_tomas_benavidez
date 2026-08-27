from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.producto_lista_crear, name='producto_lista_crear'),
    path('productos/<int:pk>/', views.producto_detalle, name='producto_detalle'),
]
