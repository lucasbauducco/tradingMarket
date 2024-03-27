from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from ..models import CEDEAR
import json

@csrf_exempt
def modificar_ratio(request):
    if request.method == 'POST':
        # Obtiene los datos del formulario
        simbolo = request.POST.get('simbolo')
        nuevo_ratio_str = request.POST.get('nuevo_ratio')  # Los datos del formulario siempre son strings

        if not simbolo or not nuevo_ratio_str:
            return JsonResponse({"status": "error", "message": "Falta el símbolo o el nuevo ratio."}, status=400)

        try:
            nuevo_ratio = float(nuevo_ratio_str)  # Intenta convertir el ratio a float
        except ValueError:
            return JsonResponse({"status": "error", "message": "Formato de ratio inválido."}, status=400)

        # Encuentra y actualiza el CEDEAR
        cedear = get_object_or_404(CEDEAR, simbolo=simbolo)
        cedear.ratio = nuevo_ratio
        cedear.save()

        return JsonResponse({"status": "success", "message": f"El ratio del CEDEAR {simbolo} ha sido actualizado a {nuevo_ratio}."})

    else:
        return JsonResponse({"status": "error", "message": "Método no permitido."}, status=405)