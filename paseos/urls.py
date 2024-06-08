from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('crearPaseo/', views.crearPaseo, name='crearPaseo'),
    path('verAdmins/', views.verAdmins, name='verAdmins'),
    path('chivas/', views.chivas, name='chivas'),
    path('chivas/eliminarChiva/<str:placa>', views.eliminarChiva, name='eliminarChiva'),
    path('verPaseosAdmin/', views.verPaseosAdmin, name='verPaseosAdmin'),

    
]