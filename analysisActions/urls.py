"""
URL configuration for trading project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from .api import ActualizarCEDEARsAPI, actualizar_ratio, ActualizarDolarMEPAPI, CalcularRatioPreciosAPI, ImportarAccionesAPI, guardar_accion
from .views import ListaCedearView, ListaRatiosView, ListaAccionView,CedearAccionListView
urlpatterns = [
    path('lista-cedear/', ListaCedearView.as_view(), name='lista_cedear'),
    path('lista-accion/', ListaAccionView.as_view(), name='lista_accion'),
    path('cedears-accion/', CedearAccionListView.as_view(), name='cedears-accion'),
    path('guardar-accion/', guardar_accion, name='guardar_accion'),
    path('calcular-ratio-precios/', ListaRatiosView.as_view(), name='lista_ratios'),
    path('api/actualizar-cedears/', ActualizarCEDEARsAPI.as_view(), name='actualizar_cedears'),
    path('api/actualizar-ratio/', actualizar_ratio, name='actualizar_ratio'),
    path('api/dolar-mep/', ActualizarDolarMEPAPI.as_view(), name='dolar-mep-api'),
    path('api/calcular-ratio-precios/', CalcularRatioPreciosAPI.as_view(), name='calcular-ratio-precios'),
    path('api/importar-acciones/', ImportarAccionesAPI.as_view(), name='importar-acciones'),
    # Otras rutas de tu aplicación
]