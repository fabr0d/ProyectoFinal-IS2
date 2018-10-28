
from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('',views.iniciarSesionControlador.iniciarSesion, name= 'login'),
    path('registro',views.registrarControlador.registrar, name='registro'),
    path('inicio',views.inicio, name='inicio'),
    path('registrarIngreso',views.registrarIngresoControlador.anadirIngreso, name='registrarIngreso'),
    path('registrarEgreso',views.registrarEgresoControlador.anadirEgreso, name='registrarEgreso'),
    path('verListadoIngresos',views.verListadoControlador.verListadoIngresos, name='verListadoIngresos'),
    path('editarIngreso',views.verListadoControlador.editarIngreso, name='editarIngreso'),
    path('verListadoEgresos',views.verListadoControlador.verListadoEgresos, name='verListadoEgresos'),
    path('editarEgreso',views.verListadoControlador.editarEgreso, name='editarEgreso'),

]

