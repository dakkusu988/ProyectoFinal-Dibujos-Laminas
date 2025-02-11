# Archivo urls.py de dibujo

from django.urls import path
from .views import * # Todas las vistas
from . import views # Importado para el registro
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    # Laminas
    # Listado
    path('', listadoDibujos.as_view(), name='listadoDibujos'),
    # Detalles
    path('dibujos/<int:pk>', detallesDibujos.as_view(), name='detallesDibujos'),
    # Añadir
    path('dibujos/añadir/', login_required(añadirDibujos.as_view()), name='añadirDibujos'),
    # Editar
    path('dibujos/editar/<int:pk>/', login_required(editarDibujos.as_view()), name='editarDibujos'),
    # Borrar
    path('dibujos/borrar/<int:pk>/', login_required(borrarDibujos.as_view()), name='borrarDibujos'),
    # Perfil de Usuario
    # Detalles
    path('perfil/', login_required(detallesUsuario.as_view()), name='detallesUsuario'),
    # Editar
    path('perfil/editar/', login_required(editarUsuario.as_view()), name='editarUsuario'),
    # REGISTRO
    path('register/', views.register, name='register'),
    # ME GUSTA
    path('like-toggle/<int:dibujo_id>/', views.like_toggle, name='like-toggle'),
]