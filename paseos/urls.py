from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registrarPaseo/', views.registrarPaseo, name='registrarPaseo'),
    path('verAdmins/', views.verAdmins, name='verAdmins'),
    path('chivas/', views.chivas, name='chivas'),
    path('chivas/eliminarChiva/<int:id>', views.eliminarChiva, name='eliminarChiva'),
    path('chivas/actualizarChiva/<int:id>/', views.actualizarFormChiva, name='actualizarFormChiva'),
    path('verPaseosAdmin/', views.verPaseosAdmin, name='verPaseosAdmin'),
    path('paseoAdmin/<int:id>', views.paseoAdmin, name='paseoAdmin'),      
    path('inicioSesionAdmin/', views.inicioSesionAdmin, name='inicioSesionAdmin' ),
    path('pagosAdmin/', views.pagosAdmin, name='pagosAdmin' ),
    path('desembolsos/', views.desembolsos, name='desembolsos'),
    path('desembolsos/confirmacionDesembolso', views.confirmacionDesembolso, name='confirmacionDesembolsos')
]