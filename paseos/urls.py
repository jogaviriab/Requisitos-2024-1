from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registrarPaseo/', views.registrarPaseo, name='registrarPaseo'),
    path('verAdmins/', views.verAdmins, name='verAdmins'),
    path('chivas/', views.chivas, name='chivas'),
    path('chivas/eliminarChiva/<str:placa>', views.eliminarChiva, name='eliminarChiva'),
    path('verPaseosAdmin/', views.verPaseosAdmin, name='verPaseosAdmin'),
    path('paseoAdmin/<int:id>', views.paseoAdmin, name='paseoAdmin'),      
    path('inicioSesionAdmin', views.inicioSesionAdmin, name='inicioSesionAdmin' )
]