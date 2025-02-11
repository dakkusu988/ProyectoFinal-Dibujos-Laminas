from django import forms
from .models import *
from django.contrib.auth.models import User # Usuario por defecto
from django.contrib.auth.forms import UserCreationForm

# Formulario de los Dibujos / Láminas
class DibujoForm(forms.ModelForm):
    class Meta:
        model = Dibujo
        fields = ['nombre', 'imagen', 'genero', 'stock', 'precio']

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')

        if stock < 0:
            raise forms.ValidationError('El stock NO puede ser MENOR que 0.')
        if stock > 100:
            raise forms.ValidationError('El stock debe ser MENOR que 100.')
        
        return stock
    
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')

        if precio.precio <= 0:
            raise forms.ValidationError('El precio NO puede ser MENOR o IGUAL que 0.')
        if precio.precio > 50:
            raise forms.ValidationError('El precio debe ser MENOR que 50.')
        
        return precio

# Formulario para el Usuario por defecto
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

#Formulario para el Registro
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']