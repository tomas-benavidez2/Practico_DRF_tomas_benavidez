from django.db import models


class Producto(models.Model):
    CATEGORIAS = [
        ('pasta_fresca', 'Pasta Fresca'),
        ('pasta_rellena', 'Pasta Rellena'),
        ('salsa', 'Salsa'),
        ('postre', 'Postre'),
    ]

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, default='')
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default='pasta_fresca')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.nombre} (${self.precio})"
