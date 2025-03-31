from django.contrib import admin
from .models import *

class DibujoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'autor', 'genero', 'stock', 'precio']
    exclude = ('autor',)  # Oculta el campo 'autor' en el admin

    def save_model(self, request, obj, form, change):
        if not obj.autor_id:  # Si el autor no está definido, se asigna al usuario actual
            obj.autor = request.user
        obj.save()

admin.site.register(Dibujo, DibujoAdmin)
admin.site.register(Precio)
