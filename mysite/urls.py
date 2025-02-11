# Archivo urls.py de mysite

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include('dibujo.urls')),
  path('accounts/', include('django.contrib.auth.urls')), # PARA EL LOGIN & LOGOUT
  path('api/v1/', include('api.urls', namespace='api')),
]

# PARA LAS IMAGENES
urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)