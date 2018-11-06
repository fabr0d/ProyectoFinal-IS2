
from django.urls import path

from . import views

urlpatterns = [
    path('',views.Vista_IniciarSesion.iniciarSesion, name= 'login'),
    path('registro',views.Vista_Registrar.registrar, name='registro'),
    path('inicio',views.inicio, name='inicio'),
    path('registrarIngreso',views.Vista_RegistrarIngreso.anadirIngreso, name='registrarIngreso'),
    path('registrarEgreso',views.Vista_RegistrarEgreso.anadirEgreso, name='registrarEgreso'),
    path('verListadoIngresos',views.Vista_VerListado.verListadoIngresos, name='verListadoIngresos'),
    path('editarIngreso',views.Vista_VerListado.editarIngreso, name='editarIngreso'),
    path('verListadoEgresos',views.Vista_VerListado.verListadoEgresos, name='verListadoEgresos'),
    path('editarEgreso',views.Vista_VerListado.editarEgreso, name='editarEgreso'),

]

