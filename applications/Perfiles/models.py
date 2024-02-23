from django.db import models
from applications.RegistroUsuarios.models import Perfil



class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=30, decimal_places=2)
    ciudad = models.CharField(max_length=50)
    ubicacion_especifica = models.CharField(max_length=100, blank=False)
    autor_persona_natural = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='productos_persona_natural', null=True, blank=True)
    autor_empresa = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='productos_empresa', null=True, blank=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    categoria = models.IntegerField(choices=[(0, 'Verduras'), (1, 'Frutas')])

    def str(self):
        return self.nombre
    
class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos')


