from .models import * # Modelos
from .forms import * # Formularios
from django.views.generic import * # Template, List, Detail, Create, Update y Delete View
from django.contrib.auth.mixins import LoginRequiredMixin # Para el LOGIN & LOGOUT
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User # Usuario por defecto
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# CRUD Láminas
# HTML Listado
class listadoDibujos(ListView):
    model = Dibujo
    template_name = 'dibujo/listadoDibujos.html'
    context_object_name = 'dibujos'
    paginate_by = 4
    
    def get_queryset(self):
        queryset = super().get_queryset()

        stock = self.request.GET.get('stock')
        precio = self.request.GET.get('precio')
        search = self.request.GET.get('search')

        # Filtrar por stock
        if stock:
            if stock == "1":
                queryset = queryset.filter(stock__gt=0)  # Filtrar los dibujos con stock mayor que 0
            else:
                stock_value = int(stock)  # Convertir el valor del formulario a un entero
                queryset = queryset.filter(stock=stock_value)
        
        # Filtrar por precio
        if precio:
            queryset = queryset.filter(precio_id=precio)

        # Filtrar por barra de busqueda (nombre, genero o autor)
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(genero__icontains=search) |
                Q(autor__username__icontains=search)
            )

        return queryset
    
    # Se recojen los Me Gusta del usuario autentificado para usarlos mas tarde
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            user_likes = Like.objects.filter(user=self.request.user).values_list('dibujo_id', flat=True)
            context['user_likes'] = user_likes
        else:
            context['user_likes'] = []

        context['precios'] = Precio.objects.all()
        
        context['selected_stock'] = self.request.GET.get('stock', '') # No se han usado porque no sabía como hacerlo con ellos
        context['selected_precio'] = self.request.GET.get('precio', '') # No se han usado porque no sabía como hacerlo con ellos
        context['search_query'] = self.request.GET.get('search', '')

        return context
    
# HTML Detalles
class detallesDibujos(DetailView):
    model = Dibujo
    template_name = 'dibujo/detallesDibujos.html'
    context_object_name = 'dibujo'

    # Se recojen los Me Gusta del usuario autentificado para usarlos mas tarde
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            user_likes = Like.objects.filter(user=self.request.user).values_list('dibujo_id', flat=True)
            context['user_likes'] = user_likes
        else:
            context['user_likes'] = []

        return context

# Esto iria en detallesDibujos.html pero no funcionaba
# <!-- <p> <b>Autor:</b> <a href="{% url 'detallesUsuario' dibujo.autor.id %}">{{ dibujo.autor.username }}</a> </p> -->

# Añadir la lámina
class añadirDibujos(LoginRequiredMixin, CreateView):
    model = Dibujo
    form_class = DibujoForm
    template_name = 'dibujo/añadirDibujos.html'
    success_url = reverse_lazy('listadoDibujos')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

# Editar la lámina
class editarDibujos(LoginRequiredMixin, UpdateView):
    model = Dibujo
    form_class = DibujoForm
    template_name = 'dibujo/editarDibujos.html'
    success_url = reverse_lazy('listadoDibujos')

    # Esto hace que aunque intentes acceder al editar o borrar 
    # de otro dibujo que no es tuyo desde un enlace directo te deniega el acceso
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.autor != self.request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

# Borrar la lámina
class borrarDibujos(LoginRequiredMixin, DeleteView):
    model = Dibujo
    template_name = 'dibujo/borrarDibujos.html'
    context_object_name = 'dibujo'
    success_url = reverse_lazy('listadoDibujos')

    # Esto hace que aunque intentes acceder al editar o borrar 
    # de otro dibujo que no es tuyo desde un enlace directo te deniega el acceso
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.autor != self.request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

# Perfil de Usuario
# HTML Detalles del Perfil de Usuario
class detallesUsuario(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'dibujo/detallesUsuario.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user
    
    # Filtramos por el Autor correspondiente para que aparezcan sus Laminas y Me gusta en su perfil
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.get_object()
        context['dibujos'] = Dibujo.objects.filter(autor=usuario)
        context['me_gustas'] = Dibujo.objects.filter(like__user=usuario)
        return context

# HTML Editar el Perfil de Usuario
class editarUsuario(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'dibujo/editarUsuario.html'
    success_url = reverse_lazy('detallesUsuario')

    def get_object(self):
        return self.request.user
    
# REGISTRO DEL USUARIO (COPY DEL CLASSROOM)
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registrado con éxito")
            return redirect("/")
        messages.error(request, "Error en el registro. La información proporcionada no es válida")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})

# Funcion para Dar o Quitar el Me Gusta de la Lamina
@login_required
def like_toggle(request, dibujo_id):
    dibujo = get_object_or_404(Dibujo, id=dibujo_id)
    like, created = Like.objects.get_or_create(user=request.user, dibujo=dibujo)

    # Se quita el MG si detecta que ya se habia dado Like anteriormente
    if not created:
        like.delete()
    
    # Recarga la pagina cuando da el MG para actualizar los MG y te devuelve a la 
    # ultima pagina que estuvieses y si no la encuentra vuelves al Menu Principal
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/')) 

# Ver el Carrito
@login_required
def ver_carrito(request):
    # Obtener o crear el carrito del usuario
    carrito = Carrito.objects.filter(usuario=request.user).first()
    items = carrito.items.all() if carrito else []

    # Calcular el total sumando el precio del dibujo multiplicado por la cantidad en el carrito
    total_precio = sum(item.dibujo.precio.precio * item.cantidad for item in items)

    return render(request, 'dibujo/carrito.html', {'items': items, 'total_precio': total_precio})


# Añadir al Carrito
@login_required
def añadir_al_carrito(request, dibujo_id):
    dibujo = get_object_or_404(Dibujo, id=dibujo_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    # Verificar si ya está en el carrito
    carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, dibujo=dibujo)
    if not created:
        carrito_item.cantidad += 1
    carrito_item.save()

    return redirect('detallesDibujos', pk=dibujo_id)

# Eliminar Carrito
@login_required
def eliminar_del_carrito(request, dibujo_id):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    carrito.items.filter(dibujo_id=dibujo_id).delete()
    return redirect('ver_carrito')

# Actualizar Carrito
@login_required
def actualizar_carrito(request, dibujo_id):
    dibujo = get_object_or_404(Dibujo, id=dibujo_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, dibujo=dibujo)

    if request.POST.get('accion') == 'sumar':
        if carrito_item.cantidad < dibujo.stock:
            carrito_item.cantidad += 1

    elif request.POST.get('accion') == 'restar':
        if carrito_item.cantidad > 1:
            carrito_item.cantidad -= 1

    carrito_item.save()
    return redirect('ver_carrito')

#Confirmar Compra de los Pedidos
@login_required
def confirmar_compra(request):
    # Obtener el carrito del usuario
    carrito = Carrito.objects.filter(usuario=request.user).first()
    items = carrito.items.all() if carrito else []
    
    if request.method == "POST":
        return redirect('procesar_compra')  # Redirige a la función que generará el PDF y enviará los correos
    
    return render(request, 'dibujo/confirmar_compra.html', {'items': items})
