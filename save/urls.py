
from django.urls import path

from . import views

urlpatterns = [
    path('',views.Vista_IniciarSesion.iniciar_sesion, name= 'login'),
    path('registro',views.Vista_Registrar.registrar, name='registro'),
    path('inicio',views.Vista_inicio.inicio, name='inicio'),
    path('registrarIngreso',views.Vista_RegistrarIngreso.anadir_ingreso, name='registrarIngreso'),
    path('registrarEgreso',views.Vista_RegistrarEgreso.anadir_egreso, name='registrarEgreso'),
    path('verListadoIngresos',views.Vista_VerListado.ver_listado_ingresos, name='verListadoIngresos'),
    path('editarIngreso',views.Vista_VerListado.editar_ingreso, name='editarIngreso'),
    path('verListadoEgresos',views.Vista_VerListado.ver_listado_egresos, name='verListadoEgresos'),
    path('editarEgreso',views.Vista_VerListado.editar_egreso, name='editarEgreso'),
    path('controlEgreso',views.Vista_ControlEgresos.ver_control_egreso, name='controlEgreso'),
    path('compararPeriodos',views.Vista_CompararPeriodos.comparar_periodos, name='compararPeriodos')
]

