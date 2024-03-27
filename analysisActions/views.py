from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from .models import CEDEAR, Accion, Operacion
from django.core.paginator import Paginator
from .api import CalcularRatioPreciosAPI
from django.db.models import Q
class Operacion(ListView):
    model = Operacion
    template_name = 'operacion/lista_operacion.html'  # Asegúrate de reemplazar este nombre si es necesario
    context_object_name = 'operaciones_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
class ListaCedearView(ListView):
    model = CEDEAR
    template_name = 'cedears/lista_cedears.html'  # Asegúrate de reemplazar este nombre si es necesario
    context_object_name = 'cedears'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
class ListaAccionView(ListView):
    model = Accion
    template_name = 'acciones/lista_acciones.html'  # Asegúrate de reemplazar este nombre
    context_object_name = 'acciones'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
class ListaRatiosView(TemplateView):
    template_name = 'cedears/lista_ratios.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Instancia tu APIView que calcula los ratios y obtiene la respuesta
        calcular_ratio_api_view = CalcularRatioPreciosAPI()
        response = calcular_ratio_api_view.get(self.request)
        cedears_list = response.data

        # Enviar los datos de los CEDEARs directamente al contexto sin paginación
        context['cedears_list'] = cedears_list

        return context