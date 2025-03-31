from django.db import models
from django.core.validators import FileExtensionValidator
from django.forms import ValidationError
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Precio(models.Model):
    precio = models.DecimalField(blank=False, null=False, max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.precio}€'

# Valida la imagen en el formulario
def validate_image(value):
    if value is None:
        raise ValidationError(('Debes subir una imagen.'))
    
class Dibujo(models.Model):
    nombre = models.CharField(max_length=100)
    # imagen = models.ImageField(upload_to='imagen_dibujos/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png']), validate_image])
    imagen = CloudinaryField('imagen') # Nueva imagen para poder almacenarla en Cloudinary
    genero = models.CharField(max_length=100)
    stock = models.IntegerField(blank=False, null=False)
    precio = models.ForeignKey(Precio, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return self.nombre
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dibujo = models.ForeignKey(Dibujo, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'dibujo')

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    dibujo = models.ForeignKey(Dibujo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    agregado_en = models.DateTimeField(auto_now_add=True)