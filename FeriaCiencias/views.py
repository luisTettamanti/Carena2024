from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from .models import Proyecto, Seccion, Articulo
from .forms import seccionForm, proyectoForm, seccionFormSet, articuloForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

def index(request):
    proyectos = Proyecto.objects.all()
    context = {"proyectos": proyectos}
    return render(request, "index.html", context)


def proyecto(request, pk):
    proyectos = Proyecto.objects.all()
    proyecto = Proyecto.objects.get(id=pk)
    secciones = Seccion.objects.filter(idProyecto__nombre__icontains=proyecto.nombre)
    context = {"proyecto": proyecto, "proyectos": proyectos, "secciones": secciones}
    return render(request, "ia/proyecto.html", context)


def seccion(request, pk):
    proyectos = Proyecto.objects.all()
    # secciones = Seccion.objects.all()
    seccion = Seccion.objects.get(id=pk)
    proyecto = Proyecto.objects.get(id=seccion.idProyecto_id)
    secciones = Seccion.objects.filter(idProyecto=proyecto.id)
    articulos = Articulo.objects.filter(idSeccion__titulo__icontains=seccion.titulo)
    context = {"proyectos": proyectos, "secciones": secciones, "seccion": seccion, "articulos": articulos}
    return render(request, "ia/seccion.html", context)


def proyectosLista(request):
    proyectos = Proyecto.objects.all()
    context = {"proyectos": proyectos}
    return render(request, "proyectosLista.html", context)


def proyectoAgregar(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        imagen = request.POST.get('imagen')
        titulo = request.POST.get('titulo')
        link = request.POST.get('link')
        color = request.POST.get('color')

        # Validación simple
        if nombre and descripcion and titulo and link:
            nuevoRegistro = Proyecto(nombre=nombre, descripcion=descripcion, imagen=imagen, titulo=titulo, link=link)
            nuevoRegistro.save()
            return redirect('proyectoslista')

    return render(request, 'proyectoAgregar.html')


def proyectoModificar(request, pk):
    proyecto = get_object_or_404(Proyecto, id=pk)

    if request.method == "POST":
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        imagen = request.POST.get('imagen')
        titulo = request.POST.get('titulo')
        link = request.POST.get('link')
        color = request.POST.get('color')

        # Validación simple
        if nombre and descripcion and titulo and link:
            proyecto.nombre = nombre
            proyecto.descripcion = descripcion
            proyecto.imagen = imagen
            proyecto.titulo = titulo
            proyecto.link = link
            proyecto.color = color
            proyecto.save()
            return redirect('proyectoslista')  # Redirigir después de la actualización

    return render(request, 'proyectoModificar.html', {'proyecto': proyecto})


def proyectoBorrar(request, pk):
    proyecto = get_object_or_404(Proyecto, id=pk)

    if request.method == "POST":
        proyecto.delete()
        return redirect('proyectoslista')  # Redirigir después de la eliminación

    return render(request, 'proyectoBorrar.html', {'proyecto': proyecto})


def proyectoConLista(request, pk):
    proyecto = get_object_or_404(Proyecto, id=pk)
    secciones = Seccion.objects.filter(idProyecto=proyecto.id)

    if request.method == "POST":
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        imagen = request.POST.get('imagen')
        titulo = request.POST.get('titulo')
        link = request.POST.get('link')
        color = request.POST.get('color')

        # Validación simple
        if nombre and descripcion and titulo and link:
            proyecto.nombre = nombre
            proyecto.descripcion = descripcion
            proyecto.imagen = imagen
            proyecto.titulo = titulo
            proyecto.link = link
            proyecto.color = color
            proyecto.save()
            return redirect('proyectoslista')  # Redirigir después de la actualización

    return render(request, 'proyectoConLista.html', {'proyecto': proyecto, 'secciones': secciones})


def proyectoAgregarModif(request, pk=None):
    # Vista para cargar/modificar proyectos usando formsets.
    if pk:
        proyecto = get_object_or_404(Proyecto, pk=pk)
    else:
        proyecto = None

    if request.method == 'POST':
        proyectoform = proyectoForm(request.POST, instance=proyecto)
        seccionformset = seccionFormSet(request.POST, instance=proyecto)

        if proyectoform.is_valid() and seccionformset.is_valid():
            proyecto = proyectoform.save()
            seccionformset.instance = proyecto
            seccionformset.save()
            return redirect('proyectoslista')
    else:
        proyectoform = proyectoForm(instance=proyecto)
        seccionformset = seccionFormSet(instance=proyecto)

    return render(request, 'proyectoForm.html', {
        'proyectoform': proyectoform,
        'seccionformset': seccionformset,
    })


# def seccionesLista(request):
    # secciones = Seccion.objects.all()
    # proyectos = Proyecto.objects.all()
    # context = {"proyectos": proyectos, "secciones": secciones}
    # return render(request, "seccionesLista.html", context)


class seccionesLista(ListView):
    model = Seccion
    template_name = 'seccionesLista.html'
    context_object_name = 'secciones'
    paginate_by = 7
    extra_context = {'proyectos': Proyecto.objects.all()}

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(idProyecto=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Enviar el valor de la búsqueda al contexto
        return context


def seccionAgregar(request):
    if request.method == 'POST':
        form = seccionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('seccioneslista'))
    else:
        form = seccionForm()
    return render(request, 'seccionForm.html', {'form': form})


def seccionModificar(request, pk):
    seccion = get_object_or_404(Seccion, id=pk)
    if request.method == 'POST':
        form = seccionForm(request.POST, instance=seccion)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('seccioneslista'))
    else:
        form = seccionForm(instance=seccion)
    return render(request, 'seccionForm.html', {'form': form, 'seccion': seccion})


def seccionBorrar(request, pk):
    seccion = Seccion.objects.get(pk=pk)
    if request.method == 'POST':
        seccion.delete()
        return HttpResponseRedirect(reverse('seccionesLista'))
    return render(request, 'seccionBorrar.html', {'seccion': seccion})


class articulosLista(ListView):
    model = Articulo
    template_name = 'articulosLista.html'
    context_object_name = 'articulos'
    paginate_by = 7
    extra_context = {'proyectos': Proyecto.objects.all()}

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(titulo__icontains=query) | Q(descripcion__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Enviar el valor de la búsqueda al contexto
        return context


class articuloModificar(UpdateView):
    model = Articulo
    form_class = articuloForm
    template_name = 'articuloForm.html'
    success_url = reverse_lazy('articuloslista')


class articuloAgregar(CreateView):
    model = Articulo
    form_class = articuloForm
    template_name = 'articuloForm.html'
    success_url = reverse_lazy('articuloslista')


class articuloBorrar(DeleteView):
    model = Articulo
    template_name = 'articuloBorrar.html'
    success_url = reverse_lazy('articuloslista')