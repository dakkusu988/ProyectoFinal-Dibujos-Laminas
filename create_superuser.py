import os
import django

# Archivo creado para que se cree el usuario Admin al desplegar la Aplicación, si ya existía, no hace nada
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Datos del superusuario
username = "admin"
first_name = "Administrador"
email = "bydaxplayyt@gmail.com"
password = "admin2003"

if not User.objects.filter(username=username).exists():
    superuser = User.objects.create_superuser(username=username, email=email, password=password)
    superuser.first_name = first_name
    superuser.save()
    print("Superusuario creado correctamente.")
else:
    print("El Superusuario ya existe.")
