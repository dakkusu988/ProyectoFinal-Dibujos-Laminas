from rest_framework import serializers
from dibujo.models import Dibujo

class DibujoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Dibujo
        fields = ('nombre', 'imagen', 'genero', 'stock', 'precio', 'autor')