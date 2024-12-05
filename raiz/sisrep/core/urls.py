"""
URL configuration for sisrep project.

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

# core/urls.py

from django.urls import path
from . import views
from django.urls import path
from django.urls import path
from .views import (
    CustomLoginView, home, personalcc, generate_report, test_view,
    whaticket_view, redessociales, ventascc, ventasvirtuales,
    agregar_personal, editar_personal, eliminar_personal, delete_report,
    lista_personal_cajero, agregar_personal_cajero, editar_personal_cajero,
    eliminar_personal_cajero, delete_report_caja,
)

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('home/', home, name='home'),
    path('personalcc/', personalcc, name='personalcc'),
    path('test/', test_view, name='test_view'),
    path('reportecc/', generate_report, name='generate_report'),
    path('whaticket/', whaticket_view, name='whaticket'),
    path('redessociales/', redessociales, name='redessociales'),
    path('ventascc/', ventascc, name='ventascc'),
    path('ventasvirtuales/', ventasvirtuales, name='ventasvirtuales'),
    path('agregar_personal/', agregar_personal, name='agregar_personal'),
    path('personal_editar/<int:personal_id>/', editar_personal, name='personal_editar'),
    path('eliminar/<int:id>/', eliminar_personal, name='eliminar_personal'),
    path('delete_report/<str:zone>/', delete_report, name='delete_report'),
    path('personalcajero/', lista_personal_cajero, name='personal_cajero'),
    path('personal_cajero/agregar/', agregar_personal_cajero, name='agregar_personal_cajero'),
    path('personal_cajero/editar/<int:personal_id>/', editar_personal_cajero, name='editar_personal_cajero'),
    path('personal_cajero/eliminar/<int:personal_id>/', eliminar_personal_cajero, name='eliminar_personal_cajero'),
    path('reportecaja/', views.reporte_cajero, name='reportecaja'),
    path('delete_report_caja/<str:zone>/', delete_report_caja, name='delete_report_caja'),
    path('get-branches/', views.get_branches, name='get_branches'),
]
