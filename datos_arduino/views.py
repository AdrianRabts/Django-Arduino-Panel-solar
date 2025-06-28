from django.shortcuts import render
from .models import SensorData

def lista_datos(request):
    datos = SensorData.objects.order_by('-timestamp')[:10]  # Últimos 30
    return render(request, 'datos_arduino/lista_datos.html', {'datos': datos})