from django.shortcuts import render
from .models import SensorData

def lista_datos(request):
    datos = SensorData.objects.order_by('-timestamp')[:50]  # Últimos 50 registros
    return render(request, 'datos_arduino/lista_datos.html', {'datos': datos})
