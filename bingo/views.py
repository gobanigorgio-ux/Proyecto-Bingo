import uuid
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Jugador
from .models import Carton
from .services import generar_matriz_bingo

# Create your views here.



def holamundo(request):
    return HttpResponse("Hola mundo")

def inicio(request):
    return render(request, 'comunes/inicio.html')

def dashboard_admin(request):
    return render(request, 'administrador/dashboard_admin.html')

def finanzas(request):
    return render(request, 'negocio/control_aportes.html')

def partidas(request):
    return render(request, 'partida/sala_espera.html')

def generar_carton(request):
    if request.method == 'POST':
        matriz_nueva = generar_matriz_bingo()
        serial_unico = f"CRT-{uuid.uuid4().hex[:8].upper()}"

        Carton.objects.create(
            codigocarton=serial_unico,
            matriznumeros=matriz_nueva
        )

    return redirect('dashboard_admin')

def eliminar_carton(request, idcarton):
    if request.method == 'POST':
        carton = get_object_or_404(Carton, idcarton=idcarton)
        carton.delete()

    return redirect('dashboard_admin')