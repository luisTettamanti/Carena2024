from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.index, name='index'),

    path('ia/proyecto/<int:pk>', views.proyecto, name='proyecto'),
    path('ia/seccion/<int:pk>/', views.seccion, name='seccion'),

    path('proyectosLista/', views.proyectosLista, name='proyectoslista'),
    path('proyectoAgregar/', views.proyectoAgregar, name='proyectoagregar'),
    path('proyectoModificar/<int:pk>/', views.proyectoModificar, name='proyectomodificar'),
    path('proyectoBorrar/<int:pk>/', views.proyectoBorrar, name='proyectoborrar'),
    path('proyectoForm/<int:pk>/', views.proyectoAgregarModif, name='proyectoagregarmodif'),
    path('proyectoConLista/<int:pk>/', views.proyectoConLista, name='proyectoconlista'),

    path('seccionesLista/', views.seccionesLista, name='seccioneslista'),
    path('seccionAgregar/', views.seccionAgregar, name='seccionagregar'),
    path('seccionModificar/<int:pk>/', views.seccionModificar, name='seccionmodificar'),
    path('seccionBorrar/<int:pk>/', views.seccionBorrar, name='seccionborrar'),

    path('articulosLista/', views.articulosLista.as_view(), name='articuloslista'),
    path('articuloAgregar/', views.articuloAgregar.as_view(), name='articuloagregar'),
    path('articuloModificar/<int:pk>/', views.articuloModificar.as_view(), name='articulomodificar'),
    path('articuloBorrar/<int:pk>/', views.articuloBorrar.as_view(), name='articuloborrar'),
]