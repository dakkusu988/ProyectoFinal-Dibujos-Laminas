from .serializers import DibujoSerializers
from rest_framework import viewsets, permissions
from dibujo.models import Dibujo

class DibujoViewset(viewsets.ModelViewSet):
    queryset = Dibujo.objects.all()
    serializer_class = DibujoSerializers
    permission_classes = [permissions.AllowAny]