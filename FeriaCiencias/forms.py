from django import forms
from .models import Proyecto, Seccion, Articulo
from django.forms.models import inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm

class seccionForm(forms.ModelForm):
    class Meta:
        model = Seccion
        fields = ('__all__')
        exclude = ('id',)
        widgets = {
            # 'id': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.TextInput(attrs={'class': 'form-control'}),
            'idProyecto': forms.Select(attrs={'class': 'form-select'}),
            'link': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            # 'descripcion': forms.Textarea(attrs={'class': 'form-control', 'style': 'background-color: ivory;'}),
        }

    # def clean_titulo(self):
    #     titulo = self.cleaned_data.get('titulo')
    #     if 'IA' in titulo:
    #         raise forms.ValidationError("No se puede usar 'IA' en el titulo")
    #     return titulo


class articuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ('__all__')
        exclude = ('id',)
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'idSeccion': forms.Select(attrs={'class': 'form-select'}),
            'link': forms.TextInput(attrs={'class': 'form-control'}),
        }


class proyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'titulo', 'descripcion', 'imagen', 'link', 'color']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'imagen': forms.TextInput(attrs={'class': 'form-control'}),
            'link': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
        }

seccionFormSet = inlineformset_factory(
    Proyecto,  # El modelo padre
    Seccion,   # El modelo hijo
    # fields=['titulo', 'descripcion', 'imagen', 'link'],  # Campos del modelo Seccion
    form=seccionForm,
    extra=1,  # Número de formularios adicionales vacíos
    can_delete=True  # Permitir borrar secciones
)


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )