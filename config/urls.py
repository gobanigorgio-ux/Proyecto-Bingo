"""
URL configuration for django_prueba project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from bingo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.holamundo, name='inicio'), # Ahora carga directo en la raíz
    path('', views.inicio, name='inicio'),
    path('panel-admin/', views.dashboard_admin, name='dashboard_admin'),
    path('finanzas/', views.finanzas, name='finanzas'),
    path('partidas/', views.partidas, name='partidas'),

]
