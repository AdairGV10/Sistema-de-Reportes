from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from .models import Personal
from .forms import PersonalForm
import pandas as pd
from django.contrib import messages
from .forms import ChatForm
from .forms import PersonalCajaForm
from .forms import ReporteForm
from .models import PersonalCaja
from .forms import ZoneSelectionForm
from .forms import BranchSelectionForm
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from django.http import HttpResponse
import io
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import base64
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from .forms import ZoneSelectionForm, BranchSelectionForm

from django.utils.safestring import mark_safe
import json

from collections import defaultdict

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def form_invalid(self, form):
        messages.error(self.request, "Credenciales incorrectas. Por favor, intenta de nuevo.")
        return super().form_invalid(form)

def home(request):

    return render(request, 'core/home.html')

def personalcc(request):
    if request.method == 'POST':
        form = PersonalForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigir a la misma página o a otra después de guardar
            return redirect('nombre_de_la_vista_donde_quieres_redirigir')  # Cambia esto según tus necesidades
    else:
        form = PersonalForm()

    personal_list = Personal.objects.all()
    return render(request, 'core/personalcc.html', {'form': form, 'personal_list': personal_list})

def reportecc(request):
    return render(request, 'core/reportecc.html')

def whaticket_view(request):
    personal_list = Personal.objects.all()
    return render(request, 'core/whaticket.html', {'personal_list': personal_list})

def redessociales(request):

    return render(request, 'core/redessociales.html')

def ventascc(request):
    personal_list = Personal.objects.all()
    ventas_list = []

    if request.method == 'POST':
        ventas = {}
        for personal in personal_list:
            venta_str = request.POST.get(f'ventas_{personal.id}', '0')
            venta = int(venta_str) if venta_str.isdigit() else 0
            ventas[personal.id] = venta
        
        # Crear una lista de ventas para pasar a la plantilla
        ventas_list = [(personal.name, ventas[personal.id]) for personal in personal_list]
        
    return render(request, 'core/ventascc.html', {
        'personal_list': personal_list,
        'ventas_list': ventas_list,
    })

def ventasvirtuales(request):

    return render(request, 'core/ventasvirtuales.html')

def personalcajero(request):

    return render(request, 'core/personalcajero.html')

def lista_personal_cajero(request):
    personal_list = PersonalCaja.objects.all()
    return render(request, 'core/personalcajero.html', {'personal_list': personal_list})

def agregar_personal_cajero(request):
    if request.method == 'POST':
        form = PersonalCajaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('personal_cajero')  # Cambia esto si tu nombre de URL es diferente
    else:
        form = PersonalCajaForm()
    return render(request, 'core\personal_caja_agregar.html', {'form': form})

def editar_personal_cajero(request, personal_id):
    personal = get_object_or_404(PersonalCaja, id=personal_id)
    if request.method == 'POST':
        form = PersonalCajaForm(request.POST, instance=personal)
        if form.is_valid():
            form.save()
            return redirect('personal_cajero')
    else:
        form = PersonalCajaForm(instance=personal)
    return render(request, 'core/personal_caja_editar.html', {'form': form})

def eliminar_personal_cajero(request, personal_id):
    personal = get_object_or_404(PersonalCaja, id=personal_id)
    personal.delete()
    return redirect('personal_cajero')

def reportecaja(request):

    return render(request, 'core/reportecaja.html')

def exit(request):
    logout(request)
    return redirect('login')

def agregar_personal(request):
    if request.method == 'POST':
        form = PersonalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('personalcc')  # Redirige a la página de personal después de agregar
    else:
        form = PersonalForm()
    return render(request, 'core/personal_agregar.html', {'form': form})

def editar_personal(request, personal_id):
    personal = get_object_or_404(Personal, id=personal_id)
    if request.method == 'POST':
        form = PersonalForm(request.POST, instance=personal)
        if form.is_valid():
            form.save()
            return redirect('personalcc')
    else:
        form = PersonalForm(instance=personal)
    return render(request, 'core/personal_editar.html', {'form': form})

def eliminar_personal(request, id):
    personal = Personal.objects.get(id=id)
    personal.delete()
    return redirect('personalcc')

def test_view(request):
    return render(request, 'core/test_template.html')

#VARIABLES PARA FILTRADOD E DATOS
EXCLUDE_CATEGORIES = ['LLAMADAS DE CALIDAD']

EXCLUDE_REASONS = ['SE CORTO LLAMADA', 'NO LLEGO EL ESTADO DE CUENTA', 
                   'FELICITACION', 'SE CORTA LLAMADA EN ESPERA', 
                   'NO LLEGO FACTURA', 'LLAMADA DE CALIDAD']

COUNT_CATEGORIES = [
    'ACLARACIONES/CONSULTA',
    'QUEJAS DE SERVICIO DE TV',
    'QUEJAS DE SERVICIO DE INTERNET',
    'INSTALACIONES',
    'CANCELAR SERVICIO',
    'REDES SOCIALES'
]

COUNT_MOTIVOS_ACLARACIONES = [
    'ESTATUS DE ORDEN DE SERVICIO',
    'INFORMACION DE SUCURSALES',
    'INFORMACION DE SALDO',
    'BARRA DE CANALES',
    'INFORMACION DE PROMOCIONES / PAQUETES',
    'PAGINA WEB / REDES SOCIALES',
    'OTROS',
    'LLAMADA AVISO DE CORTE'
]

COUNT_MOTIVOS_TV = {
    'NO HAY IMAGEN PANTALLA NEGRA': ['NO HAY IMAGEN (PANTALLA NEGRA O AZUL)'],
    'IMAGEN CON LLUVIA/ NIEVE/ RAYAS/ FANTASMAS/ CONGELADA': [
        'LA IMAGEN SE VE CON LLUVIA',
        'LA IMAGEN SE VE CON NIEVE',
        'LA IMAGEN SE VE CON RAYAS',
        'LA IMAGEN SE VE CON FANTASMAS',
        'LA IMAGEN SE VE CONGELADA'
    ],
    'SOLO SE VEN ALGUNOS CANALES/SE VEN MAL/NO SE ESCUCHA/NO HAY AUDIO': [
        'SOLO SE VEN LOS CANALES LOCALES DEL 2 AL 13',
        'SE VEN MAL ALGUNOS CANALES',
        'SE ESCUCHA BIEN PERO LA IMAGEN ES MALA',
        'NO HAY AUDIO PERO SE VE LA IMAGEN BIEN'
    ],
    'MALA INSTALACIÓN': ['MALA INSTALACIÓN'],
    'CAMBIO DE CABLE VIEJO': ['CAMBIO DE CABLE VIEJO'],
    'IMAGEN DISTORSIONADA': ['IMAGEN DISTORSIONADA'],
    'FALLA GENERAL': ['FALLA GENERAL']
}

COUNT_MOTIVOS_INTERNET = {
    'NO NAVEGA LEDS FIJOS / RUIDO',
    'NO NAVEGA LEDS PARPADEANDO / NO AMARRA',
    'EQUIPO DAÑADO',
    'PENDIENTE DE INSTALAR / NO AMARRO',
    'CONFIGURACION WI-FI',
    'FALLA GENERAL'
}

COUNT_MOTIVOS_REDES = {
    'FALLA INTERNET',
    'FALLA TV',
    'SEGUIMIENTO OS',
    'INFORMACION DE SALDO',
    'MENSAJE AVISO DE CORTE',
    'FALLA GENERAL',
    'SERVICIOS Y PROMOCIONES'
}

AGENTE_NOCTURNO = [
    'CHRISTIAN OMAR'
]

def get_branches(request):
    zone = request.GET.get('zone')  # Obtener la zona de la solicitud GET
    choices = []

    if zone == 'ZONA XALTIANGUIS':
        choices = [
            ('Xaltianguis', 'Xaltianguis'),
            # ... otras sucursales
        ]
    elif zone == 'ZONA TLAXCOAPAN':
        choices = [
            ('Tlaxcoapan', 'Tlaxcoapan'),
            ('Atitalaquia', 'Atitalaquia'),
        ]
    elif zone == 'ZONA TULA DE ALLENDE':
        choices = [
            ('Tula de Allende', 'Tula de Allende'),
            ('Tezontepec de Aldama', 'Tezontepec de Aldama'),
            ('Apaxco Teleimagen', 'Apaxco Teleimagen'),
        ]

    return JsonResponse({'branches': choices})

def reportecc_view(request):
    zone_form = ZoneSelectionForm()
    branch_form = BranchSelectionForm()

    return render(request, 'reportecc.html', {
        'zone_form': zone_form,
        'branch_form': branch_form
    })

#INICIO REPORTE CALLCENTE-CALLCENTER NOCTURNO
def generate_report(request):
    agentes_bd = Personal.objects.values_list('nombre_usuario_perseo', flat=True)
    NOMBRE_AGENTE = list(agentes_bd)

    if request.method == 'POST':
        zone_form = ZoneSelectionForm(request.POST)
        if zone_form.is_valid():
            selected_zone = zone_form.cleaned_data['zone']
            branch_form = BranchSelectionForm(zone=selected_zone, data=request.POST)

            if branch_form.is_valid():
                selected_branch = branch_form.cleaned_data['branch']
                file = request.FILES.get('file')

                try:
                    df = pd.read_excel(file)
                    #LOGICA PARA EL REPORTE GENERAL, TODOS LOS AGENTES
                    # Filtrado general
                    filtered_df = df[df['NOMBRE_AGENTE'].isin(NOMBRE_AGENTE)]
                    filtered_df = filtered_df[~filtered_df['CATEGORIA_LLAMADA'].isin(EXCLUDE_CATEGORIES)]
                    filtered_df = filtered_df[~filtered_df['MOTIVO_LLAMADA'].isin(EXCLUDE_REASONS)]


                    nocturno_df = df[df['NOMBRE_AGENTE'].isin(AGENTE_NOCTURNO)]
                    nocturno_df = nocturno_df[~nocturno_df['CATEGORIA_LLAMADA'].isin(EXCLUDE_CATEGORIES)]
                    nocturno_df = nocturno_df[~nocturno_df['MOTIVO_LLAMADA'].isin(EXCLUDE_REASONS)]                 

                    # Total de llamadas de la sucursal
                    total_calls = filtered_df.shape[0]

                    # Calcular el total de llamadas por agente en la sucursal
                    calls_per_agent = (
                        filtered_df.groupby('NOMBRE_AGENTE').size().reset_index(name='total_calls')
                    )

                    filtered_df = filtered_df[filtered_df['CATEGORIA_LLAMADA'].notnull()]

                    # Calcular el total de llamadas por categoría en la sucursal
                    calls_categories = (
                        filtered_df.groupby('CATEGORIA_LLAMADA')
                        .size()
                        .reindex(COUNT_CATEGORIES, fill_value=0)
                        .reset_index(name='total_categories')
                    )

                    # Inicializar el diccionario para almacenar los totales
                    calls_categories_dict = {}

                    # Asegurar que todas las categorías en COUNT_CATEGORIES están presentes
                    for _, row in calls_categories.iterrows():
                        category = row['CATEGORIA_LLAMADA']
                        if pd.notnull(category):
                            calls_categories_dict[category] = row['total_categories']

                    # Si no hay registros, reiniciar los totales
                    if not filtered_df.empty:
                        # Si hay registros, calcula los totales como lo has hecho hasta ahora
                        calls_categories_dict = {}
                        calls_categories = (
                            filtered_df.groupby('CATEGORIA_LLAMADA')
                            .size()
                            .reindex(COUNT_CATEGORIES, fill_value=0)
                            .reset_index(name='total_categories')
                        )
                        for _, row in calls_categories.iterrows():
                            category = row['CATEGORIA_LLAMADA']
                            if pd.notnull(category):
                                calls_categories_dict[category] = row['total_categories']

                        # Acumula los valores en total_category_calls
                        total_category_calls = request.session.get(
                            'total_category_calls', {cat: 0 for cat in COUNT_CATEGORIES}
                        )
                        for category, total in calls_categories_dict.items():
                            total_category_calls[category] += total

                        # Calcula el total general de llamadas en todas las zonas
                        total_calls_all_zones = request.session.get('total_calls_all_zones', 0) + total_calls
                    else:
                        # Si no hay registros, reinicia los contadores
                        total_category_calls = {cat: 0 for cat in COUNT_CATEGORIES}
                        total_calls_all_zones = 0

                    # Calcular el total general de llamadas en todas las zonas
                    total_calls_all_zones = request.session.get('total_calls_all_zones', 0) + total_calls

                    # Calcular el total de llamadas por motivo en ACLARACIONES/CONSULTA
                    calls_motivos_aclaraciones = (
                        filtered_df[filtered_df['CATEGORIA_LLAMADA'] == 'ACLARACIONES/CONSULTA']
                        .groupby('MOTIVO_LLAMADA').size().reindex(COUNT_MOTIVOS_ACLARACIONES, fill_value=0).reset_index(name='total_motivo')
                    )

                    # Asegurar que todos los motivos en COUNT_MOTIVOS_ACLARACIONES están presentes
                    calls_motivos_dict = {motivo: 0 for motivo in COUNT_MOTIVOS_ACLARACIONES}
                    for _, row in calls_motivos_aclaraciones.iterrows():
                        motivo = row['MOTIVO_LLAMADA']
                        calls_motivos_dict[motivo] = row['total_motivo']

                    # Total de llamadas de aclaraciones en la sucursal
                    total_calls_aclaraciones = sum(calls_motivos_dict.values())

                    # Inicializar el diccionario para almacenar los totales de motivos de QUEJAS DE SERVICIO DE TV
                    calls_motivos_tv_dict = {motivo: 0 for motivo in COUNT_MOTIVOS_TV.keys()}

                    # Filtrar el DataFrame para incluir solo las quejas de servicio de TV
                    filtered_tv_df = filtered_df[filtered_df['CATEGORIA_LLAMADA'] == 'QUEJAS DE SERVICIO DE TV']

                    # Iterar sobre cada motivo principal y sus sub-motivos
                    for motivo_principal, sub_motivos in COUNT_MOTIVOS_TV.items():
                        # Contar las llamadas que coinciden con cualquiera de los sub-motivos
                        total_motivo = filtered_tv_df[filtered_tv_df['MOTIVO_LLAMADA'].isin(sub_motivos)].shape[0]
                        calls_motivos_tv_dict[motivo_principal] = total_motivo

                    # Total de llamadas de quejas de TV en la sucursal
                    total_calls_quejas_tv = sum(calls_motivos_tv_dict.values())
                    
                    # Inicializar el diccionario para almacenar los totales de motivos de QUEJAS DE SERVICIO DE INTERNET
                    calls_motivos_internet_dict = {motivo: 0 for motivo in COUNT_MOTIVOS_INTERNET}
                    
                    # Filtrar el DataFrame para incluir solo las quejas de servicio de Internet
                    filtered_internet_df = filtered_df[filtered_df['CATEGORIA_LLAMADA'] == 'QUEJAS DE SERVICIO DE INTERNET']

                    # Iterar sobre cada motivo y contar las llamadas que coinciden
                    for motivo in COUNT_MOTIVOS_INTERNET:
                        total_motivo = filtered_internet_df[filtered_internet_df['MOTIVO_LLAMADA'] == motivo].shape[0]
                        calls_motivos_internet_dict[motivo] = total_motivo
                        

                    # Total de llamadas de quejas de Internet en la sucursal
                    total_calls_quejas_internet = sum(calls_motivos_internet_dict.values())

                    # Inicializar el diccionario para almacenar los totales de motivos de redes sociales
                    calls_motivos_redes_dict = {motivo: 0 for motivo in COUNT_MOTIVOS_REDES}

                    # Filtrar el DataFrame para incluir solo las llamadas de redes sociales
                    filtered_redes_df = filtered_df[filtered_df['CATEGORIA_LLAMADA'] == 'REDES SOCIALES']

                    # Contar las llamadas para cada motivo en COUNT_MOTIVOS_REDES
                    for motivo in COUNT_MOTIVOS_REDES:
                        total_motivo = filtered_redes_df[filtered_redes_df['MOTIVO_LLAMADA'] == motivo].shape[0]
                        calls_motivos_redes_dict[motivo] = total_motivo

                    # Total de llamadas de redes sociales en la sucursal
                    total_calls_redes = sum(calls_motivos_redes_dict.values())

                    # ***************************************************************************INICIA LOGICA DE REPORTE NOCTURNO****************************************************************************
                   # Total de llamadas de la sucursal (para agentes nocturnos)
                    total_calls_nocturno = nocturno_df.shape[0]

                    # Calcular el total de llamadas por agente en la sucursal (para agentes nocturnos)
                    calls_per_agent_nocturno = (
                        nocturno_df.groupby('NOMBRE_AGENTE').size().reset_index(name='total_calls_nocturno')
                    )

                    # Calcular el total de llamadas por categoría en la sucursal (para agentes nocturnos)
                    calls_categories_nocturno = (
                        nocturno_df.groupby('CATEGORIA_LLAMADA').size().reindex(COUNT_CATEGORIES, fill_value=0).reset_index(name='total_categories_nocturno')
                    )

                    # Asegurar que todas las categorías en COUNT_CATEGORIES están presentes (para agentes nocturnos)
                    calls_categories_dict_nocturno = {cat: 0 for cat in COUNT_CATEGORIES}
                    for _, row in calls_categories_nocturno.iterrows():
                        category = row['CATEGORIA_LLAMADA']
                        calls_categories_dict_nocturno[category] = row['total_categories_nocturno']

                    # Calcular el total de llamadas por categoría en todas las zonas (incluyendo nocturno)
                    total_category_calls_nocturno = request.session.get('total_category_calls', {cat: 0 for cat in COUNT_CATEGORIES})
                    for category, total in calls_categories_dict_nocturno.items():
                        total_category_calls_nocturno[category] += total

                    # Calcular el total general de llamadas en todas las zonas (incluyendo nocturno)
                    total_calls_all_zones_nocturno = request.session.get('total_calls_all_zones', 0) + total_calls_nocturno
                    
                    # Calcular el total de llamadas por motivo en ACLARACIONES/CONSULTA para agentes nocturnos
                    calls_motivos_aclaraciones_nocturno = (
                        nocturno_df[nocturno_df['CATEGORIA_LLAMADA'] == 'ACLARACIONES/CONSULTA']
                        .groupby('MOTIVO_LLAMADA').size().reindex(COUNT_MOTIVOS_ACLARACIONES, fill_value=0).reset_index(name='total_motivo_nocturno')
                    )

                    # Asegurar que todos los motivos en COUNT_MOTIVOS_ACLARACIONES están presentes para agentes nocturnos
                    calls_motivos_dict_nocturno = {motivo: 0 for motivo in COUNT_MOTIVOS_ACLARACIONES}
                    for _, row in calls_motivos_aclaraciones_nocturno.iterrows():
                        motivo = row['MOTIVO_LLAMADA']
                        calls_motivos_dict_nocturno[motivo] = row['total_motivo_nocturno']

                    # Total de llamadas de aclaraciones en la sucursal para agentes nocturnos
                    total_calls_aclaraciones_nocturno = sum(calls_motivos_dict_nocturno.values())

                    # Inicializar el diccionario para almacenar los totales de motivos de QUEJAS DE SERVICIO DE TV para agentes nocturnos
                    calls_motivos_tv_dict_nocturno = {motivo: 0 for motivo in COUNT_MOTIVOS_TV.keys()}

                    # Filtrar el DataFrame para incluir solo las quejas de servicio de TV para agentes nocturnos
                    filtered_tv_nocturno_df = nocturno_df[nocturno_df['CATEGORIA_LLAMADA'] == 'QUEJAS DE SERVICIO DE TV']

                    # Iterar sobre cada motivo principal y sus sub-motivos para agentes nocturnos
                    for motivo_principal, sub_motivos in COUNT_MOTIVOS_TV.items():
                        # Contar las llamadas que coinciden con cualquiera de los sub-motivos para agentes nocturnos
                        total_motivo_nocturno = filtered_tv_nocturno_df[filtered_tv_nocturno_df['MOTIVO_LLAMADA'].isin(sub_motivos)].shape[0]
                        calls_motivos_tv_dict_nocturno[motivo_principal] = total_motivo_nocturno

                    # Total de llamadas de quejas de TV en la sucursal para agentes nocturnos
                    total_calls_quejas_tv_nocturno = sum(calls_motivos_tv_dict_nocturno.values())

                    # Inicializar el diccionario para almacenar los totales de motivos de QUEJAS DE SERVICIO DE INTERNET para agentes nocturnos
                    calls_motivos_internet_dict_nocturno = {motivo: 0 for motivo in COUNT_MOTIVOS_INTERNET}

                    # Filtrar el DataFrame para incluir solo las quejas de servicio de Internet para agentes nocturnos
                    filtered_internet_nocturno_df = nocturno_df[nocturno_df['CATEGORIA_LLAMADA'] == 'QUEJAS DE SERVICIO DE INTERNET']

                    # Iterar sobre cada motivo y contar las llamadas que coinciden para agentes nocturnos
                    for motivo in COUNT_MOTIVOS_INTERNET:
                        total_motivo_nocturno = filtered_internet_nocturno_df[filtered_internet_nocturno_df['MOTIVO_LLAMADA'] == motivo].shape[0]
                        calls_motivos_internet_dict_nocturno[motivo] = total_motivo_nocturno

                    # Total de llamadas de quejas de Internet en la sucursal para agentes nocturnos
                    total_calls_quejas_internet_nocturno = sum(calls_motivos_internet_dict_nocturno.values())

                    # Inicializar el diccionario para almacenar los totales de motivos de redes sociales para agentes nocturnos
                    calls_motivos_redes_dict_nocturno = {motivo: 0 for motivo in COUNT_MOTIVOS_REDES}

                    # Filtrar el DataFrame para incluir solo las llamadas de redes sociales para agentes nocturnos
                    filtered_redes_nocturno_df = nocturno_df[nocturno_df['CATEGORIA_LLAMADA'] == 'REDES SOCIALES']

                    # Contar las llamadas para cada motivo en COUNT_MOTIVOS_REDES para agentes nocturnos
                    for motivo in COUNT_MOTIVOS_REDES:
                        total_motivo_nocturno = filtered_redes_nocturno_df[filtered_redes_nocturno_df['MOTIVO_LLAMADA'] == motivo].shape[0]
                        calls_motivos_redes_dict_nocturno[motivo] = total_motivo_nocturno

                    # Total de llamadas de redes sociales en la sucursal para agentes nocturnos
                    total_calls_redes_nocturno = sum(calls_motivos_redes_dict_nocturno.values())

                    # Gestión de informes en la sesión
                    reports = request.session.get('reports', [])
                    zone_found = False

                    for report in reports:
                        if report['zone'] == selected_zone:
                            branch_found = False
                            for branch in report['branches']:
                                if branch['branch'] == selected_branch:
                                    # Actualizamos los datos de la sucursal existente para las llamadas diurnas
                                    branch['agents'] = calls_per_agent.to_dict('records')  # Llamadas diurnas
                                    branch['categories'] = [{'category': cat, 'total_categories': calls_categories_dict.get(cat, 0)} for cat in COUNT_CATEGORIES]
                                    branch['motivo_calls'] = calls_motivos_dict
                                    branch['total_calls_aclaraciones'] = total_calls_aclaraciones
                                    branch['motivo_calls_tv'] = calls_motivos_tv_dict
                                    branch['total_calls_quejas_tv'] = total_calls_quejas_tv
                                    branch['motivo_calls_internet'] = calls_motivos_internet_dict
                                    branch['total_calls_quejas_internet'] = total_calls_quejas_internet
                                    branch['motivo_calls_redes'] = calls_motivos_redes_dict
                                    branch['total_calls_redes'] = total_calls_redes

                                    # Actualizamos los datos de la sucursal para las llamadas nocturnas
                                    branch['agents_nocturno'] = calls_per_agent_nocturno.to_dict('records')  # Llamadas nocturnas
                                    branch['categories_nocturno'] = [{'category': cat, 'total_categories': calls_categories_dict_nocturno.get(cat, 0)} for cat in COUNT_CATEGORIES]
                                    branch['motivo_calls_nocturno'] = calls_motivos_dict_nocturno
                                    branch['total_calls_aclaraciones_nocturno'] = total_calls_aclaraciones_nocturno
                                    branch['motivo_calls_tv_nocturno'] = calls_motivos_tv_dict_nocturno
                                    branch['total_calls_quejas_tv_nocturno'] = total_calls_quejas_tv_nocturno
                                    branch['motivo_calls_internet_nocturno'] = calls_motivos_internet_dict_nocturno
                                    branch['total_calls_quejas_internet_nocturno'] = total_calls_quejas_internet_nocturno
                                    branch['motivo_calls_redes_nocturno'] = calls_motivos_redes_dict_nocturno
                                    branch['total_calls_redes_nocturno'] = total_calls_redes_nocturno

                                    branch_found = True
                                    break

                            # Si la sucursal no se encontró, agregamos una nueva fila para esta sucursal
                            if not branch_found:
                                report['branches'].append({
                                    'branch': selected_branch,
                                    'total_calls': total_calls,  # Total de llamadas diurnas
                                    'agents': calls_per_agent.to_dict('records'),  # Llamadas diurnas
                                    'categories': [{'category': cat, 'total_categories': calls_categories_dict.get(cat, 0)} for cat in COUNT_CATEGORIES],
                                    'motivo_calls': calls_motivos_dict,
                                    'motivo_calls_tv': calls_motivos_tv_dict,
                                    'total_calls_quejas_tv': total_calls_quejas_tv,
                                    'motivo_calls_internet': calls_motivos_internet_dict,
                                    'total_calls_quejas_internet': total_calls_quejas_internet,
                                    'total_calls_aclaraciones': total_calls_aclaraciones,
                                    'motivo_calls_redes': calls_motivos_redes_dict,
                                    'total_calls_redes': total_calls_redes,

                                    # Añadimos los datos de las llamadas nocturnas
                                    'total_calls_nocturno': total_calls_nocturno,  # Total de llamadas nocturnas
                                    'agents_nocturno': calls_per_agent_nocturno.to_dict('records'),  # Llamadas nocturnas
                                    'categories_nocturno': [{'category': cat, 'total_categories': calls_categories_dict_nocturno.get(cat, 0)} for cat in COUNT_CATEGORIES],
                                    'motivo_calls_nocturno': calls_motivos_dict_nocturno,
                                    'motivo_calls_tv_nocturno': calls_motivos_tv_dict_nocturno,
                                    'total_calls_quejas_tv_nocturno': total_calls_quejas_tv_nocturno,
                                    'motivo_calls_internet_nocturno': calls_motivos_internet_dict_nocturno,
                                    'total_calls_quejas_internet_nocturno': total_calls_quejas_internet_nocturno,
                                    'total_calls_aclaraciones_nocturno': total_calls_aclaraciones_nocturno,
                                    'motivo_calls_redes_nocturno': calls_motivos_redes_dict_nocturno,
                                    'total_calls_redes_nocturno': total_calls_redes_nocturno,
                                })
                            zone_found = True
                            break

                    if not zone_found:
                        reports.append({
                            'zone': selected_zone,
                            'branches': [{
                                'branch': selected_branch,
                                'total_calls': total_calls,  # Total de llamadas diurnas
                                'agents': calls_per_agent.to_dict('records'),  # Llamadas diurnas
                                'categories': [{'category': cat, 'total_categories': calls_categories_dict.get(cat, 0)} for cat in COUNT_CATEGORIES],
                                'motivo_calls': calls_motivos_dict,
                                'motivo_calls_tv': calls_motivos_tv_dict,
                                'total_calls_quejas_tv': total_calls_quejas_tv,
                                'motivo_calls_internet': calls_motivos_internet_dict,
                                'total_calls_quejas_internet': total_calls_quejas_internet,
                                'total_calls_aclaraciones': total_calls_aclaraciones,
                                'motivo_calls_redes': calls_motivos_redes_dict,
                                'total_calls_redes': total_calls_redes,

                                # Añadimos los datos de las llamadas nocturnas
                                'total_calls_nocturno': total_calls_nocturno,  # Total de llamadas nocturnas
                                'agents_nocturno': calls_per_agent_nocturno.to_dict('records'),  # Llamadas nocturnas
                                'categories_nocturno': [{'category': cat, 'total_categories': calls_categories_dict_nocturno.get(cat, 0)} for cat in COUNT_CATEGORIES],
                                'motivo_calls_nocturno': calls_motivos_dict_nocturno,
                                'motivo_calls_tv_nocturno': calls_motivos_tv_dict_nocturno,
                                'total_calls_quejas_tv_nocturno': total_calls_quejas_tv_nocturno,
                                'motivo_calls_internet_nocturno': calls_motivos_internet_dict_nocturno,
                                'total_calls_quejas_internet_nocturno': total_calls_quejas_internet_nocturno,
                                'total_calls_aclaraciones_nocturno': total_calls_aclaraciones_nocturno,
                                'motivo_calls_redes_nocturno': calls_motivos_redes_dict_nocturno,
                                'total_calls_redes_nocturno': total_calls_redes_nocturno,
                            }]
                        })

                    # Guardar los datos en la sesión
                    request.session['reports'] = reports
                    request.session['total_category_calls'] = total_category_calls
                    request.session['total_calls_all_zones'] = total_calls_all_zones
                    request.session['total_calls_all_zones_nocturno'] = total_calls_all_zones_nocturno
                    request.session.modified = True

                    return redirect('generate_report')

                    

                except Exception as e:
                    error_message = f"Error al procesar el archivo: {str(e)}"
                    return render(request, 'core/reportecc.html', {
                        'zone_form': zone_form,
                        'branch_form': branch_form,
                        'error_message': error_message
                    })

    reports = request.session.get('reports', [])
    total_category_calls = request.session.get('total_category_calls', {cat: 0 for cat in COUNT_CATEGORIES})
    total_category_calls_nocturno = request.session.get('total_category_calls_nocturno', {cat: 0 for cat in COUNT_CATEGORIES})
    total_calls_all_zones = request.session.get('total_calls_all_zones', 0)
    total_calls_all_zones_nocturno = request.session.get('total_call_all_zones_nocturno', 0)
    zone_form = ZoneSelectionForm()
    branch_form = BranchSelectionForm()

    total_calls_por_sucursal = []
    for report in reports:
        for branch in report['branches']:
            # Total de llamadas diurnas y nocturnas por sucursal
            total_calls_por_sucursal.append({
                'branch': branch['branch'],  # Nombre de la sucursal
                'total_calls': branch['total_calls'],  # Llamadas diurnas
                #'total_calls_nocturno': branch['total_calls_nocturno'],  # Llamadas nocturnas (si se necesita)
            })

    imagenes_graficas_html = []
    imagenes_graficas_excel = []  # Flujos binarios para el Excel

    for report in reports:
        selected_zone = report['zone']
        sucursales_por_zona = [
            {'branch': branch['branch'], 'total_calls': branch['total_calls']}
            for branch in report['branches']
        ]

        if not sucursales_por_zona:
            continue

        # Generar las gráficas
        imagen_base64, img_stream_excel = generar_grafico_llamadas_por_tabla(sucursales_por_zona, selected_zone)
        imagenes_graficas_html.append(imagen_base64)  # Para el HTML
        imagenes_graficas_excel.append(img_stream_excel)  # Para el Excel

    totals_per_agent_by_zone = {}
    for report in reports:
        zone = report['zone']  # Identificar la zona actual

        # Inicializar el diccionario para la zona si no existe
        if zone not in totals_per_agent_by_zone:
            totals_per_agent_by_zone[zone] = {}

        # Iterar sobre las sucursales de la zona
        for branch in report['branches']:
            for agent_data in branch['agents']:
                agent = agent_data['NOMBRE_AGENTE']  # Obtener el nombre del agente
                total_calls = agent_data['total_calls']  # Obtener las llamadas del agente en esta sucursal

                # Sumar las llamadas al agente en esta zona
                if agent in totals_per_agent_by_zone[zone]:
                    totals_per_agent_by_zone[zone][agent] += total_calls
                else:
                    totals_per_agent_by_zone[zone][agent] = total_calls

    imagenes_graficas_agentes_html = []
    imagenes_graficas_agentes_excel = []

    for zone, agent_data in totals_per_agent_by_zone.items():
        image_base64, img_stream_excel = generar_grafico_llamadas_por_agente(agent_data, zone)
        imagenes_graficas_agentes_html.append(image_base64)
        imagenes_graficas_agentes_excel.append(img_stream_excel)  # Para el Excel

    # Almacenar el total por agente por zona en la sesión si lo necesitas
    request.session['totals_per_agent_by_zone'] = totals_per_agent_by_zone
    request.session.modified = True

    imagenes_graficas_categoria = []
    imagenes_graficas_categoria_excel = []

    # Verificar si hay datos en reports
    if reports:
        for report in reports:
            # Asegurarse de que siempre exista un valor para selected_zone
            selected_zone = report.get('zone', 'Zona desconocida')  # Valor por defecto
            
            # Inicializar la lista de categorías por sucursal
            categorias_por_sucursal = []

            # Recopilar datos de las categorías por sucursal
            if 'branches' in report:
                for branch in report['branches']:
                    if 'categories' in branch:
                        for category_data in branch['categories']:
                            categorias_por_sucursal.append({
                                'category': category_data['category'],
                                'total_categories': category_data['total_categories']
                            })

            # Generar gráfica si hay datos
            if categorias_por_sucursal:  # Solo generar gráfica si hay datos
                img_base64, img_stream_excel= generar_grafico_llamadas_por_categoria(categorias_por_sucursal, selected_zone)
                imagenes_graficas_categoria.append(img_base64)
                imagenes_graficas_categoria_excel.append(img_stream_excel)
    else:
        # Manejo del caso donde no hay datos
        selected_zone = 'Zona desconocida'  # Valor por defecto para evitar errores
        categorias_por_sucursal = []  # Asegurar que esté definida como una lista vacía

    imagenes_graficas_motivos = []
    imagenes_graficas_motivos_excel = []

    # Generar gráficos por cada zona
    if reports:
        for report in reports:
            selected_zone = report.get('zone', 'Zona desconocida')
            calls_motivos_dict = defaultdict(int)

            # Recopilar datos de los motivos por sucursal
            if 'branches' in report:
                for branch in report['branches']:
                    if 'total_calls_aclaraciones' in branch and 'motivo_calls' in branch:
                        for motivo, total in branch['motivo_calls'].items():
                            calls_motivos_dict[motivo] += total

            # Crear gráfica si hay datos
            if calls_motivos_dict:
                img_base64, img_stream_excel = generar_grafico_motivos_por_zona(calls_motivos_dict, selected_zone)
                imagenes_graficas_motivos.append(img_base64)
                imagenes_graficas_motivos_excel.append(img_stream_excel)

    imagenes_graficas_motivos_tv = []
    imagenes_graficas_motivos_tv_excel = []
    # Generar gráficos de quejas de TV por cada zona
    if reports:
        for report in reports:
            selected_zone = report.get('zone', 'Zona desconocida')
            calls_motivos_tv_dict = defaultdict(int)

            # Recopilar datos de los motivos de quejas de TV por sucursal
            if 'branches' in report:
                for branch in report['branches']:
                    if 'total_calls_quejas_tv' in branch and 'motivo_calls_tv' in branch:
                        for motivo, total in branch['motivo_calls_tv'].items():
                            calls_motivos_tv_dict[motivo] += total

            # Crear gráfica si hay datos
            if calls_motivos_tv_dict:
                img_base64, img_stream_excel = generar_grafico_motivos_tv_por_zona(calls_motivos_tv_dict, selected_zone)
                imagenes_graficas_motivos_tv.append(img_base64)
                imagenes_graficas_motivos_tv_excel.append(img_stream_excel)

    imagenes_graficas_motivos_internet = []
    imagenes_graficas_motivos_internet_excel = []
    # Generar gráficos de quejas de Internet por cada zona
    if reports:
        for report in reports:
            selected_zone = report.get('zone', 'Zona desconocida')
            calls_motivos_internet_dict = defaultdict(int)

            # Recopilar datos de los motivos de quejas de Internet por sucursal
            if 'branches' in report:
                for branch in report['branches']:
                    if 'total_calls_quejas_internet' in branch and 'motivo_calls_internet' in branch:
                        for motivo, total in branch['motivo_calls_internet'].items():
                            calls_motivos_internet_dict[motivo] += total

            # Crear gráfica si hay datos
            if calls_motivos_internet_dict:
                img_base64, img_stream_excel = generar_grafico_motivos_internet_por_zona(calls_motivos_internet_dict, selected_zone)
                imagenes_graficas_motivos_internet.append(img_base64)
                imagenes_graficas_motivos_internet_excel.append(img_stream_excel)
    
    imagenes_graficas_motivos_redes = []
    imagenes_graficas_motivos_redes_excel = []
    # Generar gráficos de llamadas de redes sociales por cada zona
    if reports:
        for report in reports:
            selected_zone = report.get('zone', 'Zona desconocida')
            calls_motivos_redes_dict = defaultdict(int)

            # Recopilar datos de los motivos de redes sociales por sucursal
            if 'branches' in report:
                for branch in report['branches']:
                    if 'total_calls_redes' in branch and 'motivo_calls_redes' in branch:
                        for motivo, total in branch['motivo_calls_redes'].items():
                            calls_motivos_redes_dict[motivo] += total

            # Crear gráfica si hay datos
            if calls_motivos_redes_dict:
                img_base64, img_stream_excel = generar_grafico_motivos_redes_por_zona(calls_motivos_redes_dict, selected_zone)
                imagenes_graficas_motivos_redes.append(img_base64)
                imagenes_graficas_motivos_redes_excel.append(img_stream_excel)

    imagenes_graficas_llamadas_nocturno = []
    imagenes_graficas_llamadas_nocturno_excel = []
    # Generar gráficos de llamadas nocturnas por sucursal para cada zona
    if reports:
        for report in reports:
            selected_zone = report.get('zone', 'Zona desconocida')

            # Recopilar totales de llamadas nocturnas por sucursal
            branch_totals = []
            if 'branches' in report:
                for branch in report['branches']:
                    if 'total_calls_nocturno' in branch:
                        branch_totals.append({
                            'branch': branch['branch'],
                            'total_calls_nocturno': branch['total_calls_nocturno']
                        })

            # Crear gráfica si hay datos
            if branch_totals:
                img_base64, img_stream_excel = generar_grafico_llamadas_nocturno_por_sucursal(branch_totals, selected_zone)
                imagenes_graficas_llamadas_nocturno.append(img_base64)
                imagenes_graficas_llamadas_nocturno_excel.append(img_stream_excel)

    imagenes_graficas_categorias_nocturno = []
    imagenes_graficas_categorias_nocturno_excel = []
    # Generar gráficos de categorías nocturnas por cada zona
    if reports:
        for report in reports:
            selected_zone = report.get('zone', 'Zona desconocida')

            # Recopilar totales de llamadas por categoría en el turno nocturno
            calls_categories_dict_nocturno = defaultdict(int)
            if 'branches' in report:
                for branch in report['branches']:
                    if 'categories_nocturno' in branch:
                        for category_data in branch['categories_nocturno']:
                            category = category_data['category']
                            total = category_data['total_categories']
                            calls_categories_dict_nocturno[category] += total

            # Crear gráfica si hay datos
            if calls_categories_dict_nocturno:
                img_base64, img_stream_excel = generar_grafico_categorias_nocturno(calls_categories_dict_nocturno, selected_zone)
                imagenes_graficas_categorias_nocturno.append(img_base64)
                imagenes_graficas_categorias_nocturno_excel.append(img_stream_excel)
    
    imagenes_graficas_aclaraciones_nocturno = []
    imagenes_graficas_aclaraciones_nocturno_excel = []
    # Generar gráficos de motivos de Aclaraciones/Consultas nocturnas por cada zona
    if reports:
        for report in reports:
            selected_zone = report.get('zone', 'Zona desconocida')

            # Recopilar totales de motivos nocturnos para aclaraciones/consultas
            calls_motivos_dict_nocturno = defaultdict(int)
            if 'branches' in report:
                for branch in report['branches']:
                    if 'total_calls_aclaraciones_nocturno' in branch and 'motivo_calls_nocturno' in branch:
                        for motivo, total in branch['motivo_calls_nocturno'].items():
                            calls_motivos_dict_nocturno[motivo] += total

            # Crear gráfica si hay datos
            if calls_motivos_dict_nocturno:
                img_base64, img_stream_excel = generar_grafico_aclaraciones_nocturno(calls_motivos_dict_nocturno, selected_zone)
                imagenes_graficas_aclaraciones_nocturno.append(img_base64)
                imagenes_graficas_aclaraciones_nocturno_excel.append(img_stream_excel)

    imagenes_graficas_quejas_tv_nocturno = []
    imagenes_graficas_quejas_tv_nocturno_excel = []
    # Generar gráficos de motivos principales de quejas de TV nocturnas por cada zona
    if reports:
        for report in reports:
            selected_zone = report.get('zone', 'Zona desconocida')

            # Recopilar totales de motivos nocturnos para quejas de TV
            calls_motivos_tv_dict_nocturno = defaultdict(int)
            if 'branches' in report:
                for branch in report['branches']:
                    if 'motivo_calls_tv_nocturno' in branch:
                        for motivo, total in branch['motivo_calls_tv_nocturno'].items():
                            calls_motivos_tv_dict_nocturno[motivo] += total

            # Crear gráfica si hay datos
            if calls_motivos_tv_dict_nocturno:
                img_base64, img_stream_excel = generar_grafico_quejas_tv_nocturno(calls_motivos_tv_dict_nocturno, selected_zone)
                imagenes_graficas_quejas_tv_nocturno.append(img_base64)
                imagenes_graficas_quejas_tv_nocturno_excel.append(img_stream_excel)

    imagenes_graficas_quejas_internet_nocturno = []
    imagenes_graficas_quejas_internet_nocturno_excel = []
    # Generar gráficos de motivos de quejas de Internet nocturnas por cada zona
    if reports:
        for report in reports:
            selected_zone = report.get('zone', 'Zona desconocida')

            # Recopilar totales de motivos nocturnos para quejas de Internet
            calls_motivos_internet_dict_nocturno = defaultdict(int)
            if 'branches' in report:
                for branch in report['branches']:
                    if 'motivo_calls_internet_nocturno' in branch:
                        for motivo, total in branch['motivo_calls_internet_nocturno'].items():
                            calls_motivos_internet_dict_nocturno[motivo] += total

            # Crear gráfica si hay datos
            if calls_motivos_internet_dict_nocturno:
                img_base64, img_stream_excel = generar_grafico_quejas_internet_nocturno(calls_motivos_internet_dict_nocturno, selected_zone)
                imagenes_graficas_quejas_internet_nocturno.append(img_base64)
                imagenes_graficas_quejas_internet_nocturno_excel.append(img_stream_excel)

    imagenes_graficas_redes_nocturno = []
    imagenes_graficas_redes_nocturno_excel= []
    # Generar gráficos de motivos de redes sociales nocturnas por cada zona
    if reports:
        for report in reports:
            selected_zone = report.get('zone', 'Zona desconocida')

            # Recopilar totales de motivos nocturnos para redes sociales
            calls_motivos_redes_dict_nocturno = defaultdict(int)
            if 'branches' in report:
                for branch in report['branches']:
                    if 'motivo_calls_redes_nocturno' in branch:
                        for motivo, total in branch['motivo_calls_redes_nocturno'].items():
                            calls_motivos_redes_dict_nocturno[motivo] += total

            # Crear gráfica si hay datos
            if calls_motivos_redes_dict_nocturno:
                img_base64, img_stream_excel = generar_grafico_redes_nocturno(calls_motivos_redes_dict_nocturno, selected_zone)
                imagenes_graficas_redes_nocturno.append(img_base64)
                imagenes_graficas_redes_nocturno_excel.append(img_stream_excel)

    # Llamada a render con el contexto combinado
    return render(request, 'core/reportecc.html', {
        'zone_form': zone_form,
        'branch_form': branch_form,
        'reports': reports,
        'total_category_calls': total_category_calls,
        'total_category_calls_nocturno': total_category_calls_nocturno,
        'total_calls_all_zones': total_calls_all_zones,
        'total_calls_all_zones_nocturno': total_calls_all_zones_nocturno,
        'count_motivos_aclaraciones': COUNT_MOTIVOS_ACLARACIONES,
        'imagenes_graficas': imagenes_graficas_html,
        'imagenes_graficas_excel': imagenes_graficas_excel,  # Sólo se usará al exportar
        'imagenes_graficas_agentes': imagenes_graficas_agentes_html,
        'imagenes_graficas_agentes_excel': imagenes_graficas_agentes_excel, #Solo se usará al exportar
        'imagenes_graficas_categoria': imagenes_graficas_categoria,
        'imagenes_graficas_categoria_excel': imagenes_graficas_categoria_excel, #Solo se usará al exportar
        'imagenes_graficas_motivos': imagenes_graficas_motivos,
        'imagenes_graficas_motivos_excel': imagenes_graficas_motivos_excel,#Solo se usará al exportar
        'imagenes_graficas_motivos_tv': imagenes_graficas_motivos_tv,
        'imagenes_graficas_motivos_tv_excel': imagenes_graficas_motivos_tv_excel,#solo se usará al exportar
        'imagenes_graficas_motivos_internet': imagenes_graficas_motivos_internet,
        'imagenes_graficas_motivos_internet_excel': imagenes_graficas_motivos_internet_excel,#solo se usará al exportar
        'imagenes_graficas_motivos_redes': imagenes_graficas_motivos_redes,
        'imagenes_graficas_motivos_redes_excel' :imagenes_graficas_motivos_redes_excel,#Solo se usará al exportar
        'imagenes_graficas_llamadas_nocturno': imagenes_graficas_llamadas_nocturno,
        'imagenes_graficas_llamadas_nocturno_excel': imagenes_graficas_llamadas_nocturno_excel, # Solo se usará al exportar
        'imagenes_graficas_categorias_nocturno': imagenes_graficas_categorias_nocturno,
        'imagenes_graficas_categorias_nocturno_excel': imagenes_graficas_categorias_nocturno_excel,# Solo se usará al exportar
        'imagenes_graficas_aclaraciones_nocturno': imagenes_graficas_aclaraciones_nocturno,
        'imagenes_graficas_aclaraciones_nocturno_excel': imagenes_graficas_aclaraciones_nocturno_excel,# Solo se usará al exportar
        'imagenes_graficas_quejas_tv_nocturno': imagenes_graficas_quejas_tv_nocturno,
        'imagenes_graficas_quejas_tv_nocturno_excel':  imagenes_graficas_quejas_tv_nocturno_excel,#Solo se usará al exportar
        'imagenes_graficas_quejas_internet_nocturno': imagenes_graficas_quejas_internet_nocturno,
        'imagenes_graficas_quejas_internet_nocturno_excel': imagenes_graficas_quejas_internet_nocturno_excel,# Solo se usará al exportar
        'imagenes_graficas_redes_nocturno': imagenes_graficas_redes_nocturno,
        'imagenes_graficas_redes_nocturno_excel': imagenes_graficas_redes_nocturno_excel,#solo se usará al exportar

    })

#GRAFICAS DE REPORTE CALL-CENTER

def generar_grafico_llamadas_por_tabla(sucursales_por_zona, zona):
    if not sucursales_por_zona:
        return None  # No generar la gráfica si no hay datos

    llamadas_por_sucursal = {branch['branch']: branch['total_calls'] for branch in sucursales_por_zona}

    labels = list(llamadas_por_sucursal.keys())
    sizes = list(llamadas_por_sucursal.values())
    colors = ['#66b3ff', '#99ccff', '#cce6ff', '#e6f2ff']

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops={'edgecolor': 'black'})
    ax.set_title(f'Total de Llamadas Diurnas por Sucursal - {zona}')

    # Guardar la imagen en Base64 para el HTML
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)

    # Base64 para mostrar en HTML
    imagen_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')

    # Guardar la imagen binaria para el Excel (dejar el flujo abierto para Excel)
    img_stream_excel = io.BytesIO()
    plt.savefig(img_stream_excel, format='png')
    img_stream_excel.seek(0)

    plt.close(fig)

    return imagen_base64, img_stream_excel

def generar_grafico_llamadas_por_agente(data, zone):
    agents = list(data.keys())
    total_calls = list(data.values())

    plt.figure(figsize=(10, 6))
    plt.bar(agents, total_calls, color='skyblue', edgecolor='black')
    plt.title(f"Llamadas por agente - Zona {zone}")
    plt.xlabel("Agente")
    plt.ylabel("Total de llamadas")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Generar la imagen en memoria
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    # Convertir la imagen a base64
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    # Guardar la imagen binaria para el Excel (dejar el flujo abierto para Excel)
    img_stream_excel = io.BytesIO()
    plt.savefig(img_stream_excel, format='png')
    img_stream_excel.seek(0)

    buffer.close()

    # Retornar la imagen como cadena base64
    return image_base64, img_stream_excel

def generar_grafico_llamadas_por_categoria(categorias_por_sucursal, zone):
    # Agrupar categorías y sumar totales
    totales_por_categoria = defaultdict(int)
    for category_data in categorias_por_sucursal:
        totales_por_categoria[category_data['category']] += category_data['total_categories']

    # Ordenar las categorías para consistencia (opcional)
    categorias = list(totales_por_categoria.keys())
    totales = list(totales_por_categoria.values())

    # Crear la gráfica
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(categorias, totales, color='skyblue', edgecolor='black')

    # Configuración de la gráfica
    ax.set_xlabel('Categorías de Llamadas')
    ax.set_ylabel('Total de Llamadas')
    ax.set_title(f'Total de Llamadas por Categoría - {zone}')
    ax.set_xticklabels(categorias, rotation=45, ha='right')

    # Guardar la gráfica como imagen en base64
    img_buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)

    img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')
    plt.close(fig)  # Cerrar la figura para liberar recursos

     # Guardar la imagen binaria para el Excel (dejar el flujo abierto para Excel)
    img_stream_excel = io.BytesIO()
    plt.savefig(img_stream_excel, format='png')
    img_stream_excel.seek(0)


    # Devolver la imagen en base64
    return img_base64, img_stream_excel

def generar_grafico_motivos_por_zona(calls_motivos_dict, zone):
    # Extraer motivos y totales para la gráfica
    motivos = list(calls_motivos_dict.keys())
    totales = list(calls_motivos_dict.values())

    # Crear la gráfica
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(motivos, totales, color='skyblue', edgecolor='black')

    # Configuración de la gráfica
    ax.set_xlabel('Motivos de Llamadas', fontsize=12)
    ax.set_ylabel('Total de Llamadas', fontsize=12)
    ax.set_title(f'Total de Llamadas por Motivo en Aclaraciones/Consultas - Zona {zone}', fontsize=14)
    ax.set_xticks(range(len(motivos)))
    ax.set_xticklabels(motivos, rotation=45, ha='right')
    plt.tight_layout()

    # Convertir la gráfica a imagen base64
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', bbox_inches='tight')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')
    plt.close(fig)

     # Guardar la imagen binaria para el Excel (dejar el flujo abierto para Excel)
    img_stream_excel = io.BytesIO()
    plt.savefig(img_stream_excel, format='png')
    img_stream_excel.seek(0)

    # Retornar la imagen como cadena base64
    return img_base64, img_stream_excel

def generar_grafico_motivos_tv_por_zona(calls_motivos_tv_dict, zone):

    # Extraer motivos y totales para la gráfica
    motivos = list(calls_motivos_tv_dict.keys())
    totales = list(calls_motivos_tv_dict.values())

    # Crear la gráfica
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(motivos, totales, color='skyblue', edgecolor='black')

    # Configuración de la gráfica
    ax.set_xlabel('Motivos de Quejas de TV', fontsize=12)
    ax.set_ylabel('Total de Quejas', fontsize=12)
    ax.set_title(f'Total de Quejas por Motivo - Zona {zone}', fontsize=14)
    ax.set_xticks(range(len(motivos)))
    ax.set_xticklabels(motivos, rotation=45, ha='right')
    plt.tight_layout()

    # Convertir la gráfica a imagen base64
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', bbox_inches='tight')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')
    plt.close(fig)

         # Guardar la imagen binaria para el Excel (dejar el flujo abierto para Excel)
    img_stream_excel = io.BytesIO()
    plt.savefig(img_stream_excel, format='png')
    img_stream_excel.seek(0)

    # Retornar la imagen como cadena base64
    return img_base64, img_stream_excel

def generar_grafico_motivos_internet_por_zona(calls_motivos_internet_dict, zone):

    # Extraer motivos y totales para la gráfica
    motivos = list(calls_motivos_internet_dict.keys())
    totales = list(calls_motivos_internet_dict.values())

    # Crear la gráfica
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(motivos, totales, color='skyblue', edgecolor='black')

    # Configuración de la gráfica
    ax.set_xlabel('Motivos de Quejas de Internet', fontsize=12)
    ax.set_ylabel('Total de Quejas', fontsize=12)
    ax.set_title(f'Total de Quejas por Motivo - Zona {zone}', fontsize=14)
    ax.set_xticks(range(len(motivos)))
    ax.set_xticklabels(motivos, rotation=45, ha='right')
    plt.tight_layout()

    # Convertir la gráfica a imagen base64
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', bbox_inches='tight')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')
    plt.close(fig)

         # Guardar la imagen binaria para el Excel (dejar el flujo abierto para Excel)
    img_stream_excel = io.BytesIO()
    plt.savefig(img_stream_excel, format='png')
    img_stream_excel.seek(0)

    # Retornar la imagen como cadena base64
    return img_base64, img_stream_excel

def generar_grafico_motivos_redes_por_zona(calls_motivos_redes_dict, zone):
    # Extraer motivos y totales para la gráfica
    motivos = list(calls_motivos_redes_dict.keys())
    totales = list(calls_motivos_redes_dict.values())

    # Crear la gráfica
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(motivos, totales, color='skyblue', edgecolor='black')

    # Configuración de la gráfica
    ax.set_xlabel('Motivos de Redes Sociales', fontsize=12)
    ax.set_ylabel('Total de Llamadas', fontsize=12)
    ax.set_title(f'Total de Llamadas por Motivo - Zona {zone}', fontsize=14)
    ax.set_xticks(range(len(motivos)))
    ax.set_xticklabels(motivos, rotation=45, ha='right')
    plt.tight_layout()

    # Convertir la gráfica a imagen base64
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', bbox_inches='tight')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')
    plt.close(fig)

         # Guardar la imagen binaria para el Excel (dejar el flujo abierto para Excel)
    img_stream_excel = io.BytesIO()
    plt.savefig(img_stream_excel, format='png')
    img_stream_excel.seek(0)

    # Retornar la imagen como cadena base64
    return img_base64, img_stream_excel


#GRAFICAS DE REPORTE CALL-CENTER NOCTURNO
def generar_grafico_llamadas_nocturno_por_sucursal(branch_totals, zone):
    # Extraer nombres de sucursales y totales de llamadas
    sucursales = [item['branch'] for item in branch_totals]
    totales = [item['total_calls_nocturno'] for item in branch_totals]

    # Crear la gráfica de pastel
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(totales, labels=sucursales, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)

    # Configuración de la gráfica
    ax.set_title(f'Total de Llamadas Nocturnas por Sucursal - Zona {zone}', fontsize=14)
    plt.tight_layout()

    # Convertir la gráfica a imagen base64
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', bbox_inches='tight')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')
    plt.close(fig)

    img_stream_excel = io.BytesIO()
    plt.savefig(img_stream_excel, format='png')
    img_stream_excel.seek(0)

    # Retornar la imagen como cadena base64
    return img_base64, img_stream_excel

def generar_grafico_categorias_nocturno(calls_categories_dict_nocturno, zone):
    # Extraer categorías y totales para la gráfica
    categorias = list(calls_categories_dict_nocturno.keys())
    totales = list(calls_categories_dict_nocturno.values())

    # Crear la gráfica
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(categorias, totales, color='teal', edgecolor='black')

    # Configuración de la gráfica
    ax.set_xlabel('Categorías de Llamadas', fontsize=12)
    ax.set_ylabel('Total de Llamadas', fontsize=12)
    ax.set_title(f'Total de Llamadas por Categoría en CC Nocturno - Zona {zone}', fontsize=14)
    ax.set_xticks(range(len(categorias)))
    ax.set_xticklabels(categorias, rotation=45, ha='right')
    plt.tight_layout()

    # Convertir la gráfica a imagen base64
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', bbox_inches='tight')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')
    plt.close(fig)

    img_stream_excel = io.BytesIO()
    plt.savefig(img_stream_excel, format='png')
    img_stream_excel.seek(0)

    # Retornar la imagen como cadena base64
    return img_base64, img_stream_excel

def generar_grafico_aclaraciones_nocturno(calls_motivos_dict_nocturno, zone):
    # Extraer motivos y totales para la gráfica
    motivos = list(calls_motivos_dict_nocturno.keys())
    totales = list(calls_motivos_dict_nocturno.values())

    # Crear la gráfica
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(motivos, totales, color='teal', edgecolor='black')

    # Configuración de la gráfica
    ax.set_xlabel('Motivos de Llamadas', fontsize=12)
    ax.set_ylabel('Total de Llamadas', fontsize=12)
    ax.set_title(f'Total de Llamadas por Motivo en Aclaraciones/Consultas Nocturno - Zona {zone}', fontsize=14)
    ax.set_xticks(range(len(motivos)))
    ax.set_xticklabels(motivos, rotation=45, ha='right')
    plt.tight_layout()

    # Convertir la gráfica a imagen base64
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', bbox_inches='tight')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')
    plt.close(fig)

    img_stream_excel = io.BytesIO()
    plt.savefig(img_stream_excel, format='png')
    img_stream_excel.seek(0)

    # Retornar la imagen como cadena base64
    return img_base64, img_stream_excel

def generar_grafico_quejas_tv_nocturno(calls_motivos_tv_dict_nocturno, zone):
    # Extraer motivos principales y totales para la gráfica
    motivos = list(calls_motivos_tv_dict_nocturno.keys())
    totales = list(calls_motivos_tv_dict_nocturno.values())

    # Crear la gráfica
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(motivos, totales, color='teal', edgecolor='black')

    # Configuración de la gráfica
    ax.set_xlabel('Motivos de Quejas de TV', fontsize=12)
    ax.set_ylabel('Total de Llamadas', fontsize=12)
    ax.set_title(f'Total de Quejas de TV en CC Nocturno - Zona {zone}', fontsize=14)
    ax.set_xticks(range(len(motivos)))
    ax.set_xticklabels(motivos, rotation=45, ha='right')
    plt.tight_layout()

    # Convertir la gráfica a imagen base64
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', bbox_inches='tight')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')
    plt.close(fig)

    img_stream_excel = io.BytesIO()
    plt.savefig(img_stream_excel, format='png')
    img_stream_excel.seek(0)

    # Retornar la imagen como cadena base64
    return img_base64, img_stream_excel

def generar_grafico_quejas_internet_nocturno(calls_motivos_internet_dict_nocturno, zone):
        # Extraer motivos y totales para la gráfica
    motivos = list(calls_motivos_internet_dict_nocturno.keys())
    totales = list(calls_motivos_internet_dict_nocturno.values())

    # Crear la gráfica
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(motivos, totales, color='teal', edgecolor='black')

    # Configuración de la gráfica
    ax.set_xlabel('Motivos de Quejas de Internet', fontsize=12)
    ax.set_ylabel('Total de Llamadas', fontsize=12)
    ax.set_title(f'Total de Quejas de Internet en CC Nocturno - Zona {zone}', fontsize=14)
    ax.set_xticks(range(len(motivos)))
    ax.set_xticklabels(motivos, rotation=45, ha='right')
    plt.tight_layout()

    # Convertir la gráfica a imagen base64
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', bbox_inches='tight')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')
    plt.close(fig)

    img_stream_excel = io.BytesIO()
    plt.savefig(img_stream_excel, format='png')
    img_stream_excel.seek(0)

    # Retornar la imagen como cadena base64
    return img_base64, img_stream_excel

def generar_grafico_redes_nocturno(calls_motivos_redes_dict_nocturno, zone):
    # Extraer motivos y totales para la gráfica
    motivos = list(calls_motivos_redes_dict_nocturno.keys())
    totales = list(calls_motivos_redes_dict_nocturno.values())

    # Crear la gráfica
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(motivos, totales, color='teal', edgecolor='black')

    # Configuración de la gráfica
    ax.set_xlabel('Motivos de Redes Sociales', fontsize=12)
    ax.set_ylabel('Total de Llamadas', fontsize=12)
    ax.set_title(f'Total de Llamadas de Redes Sociales en CC Nocturno - Zona {zone}', fontsize=14)
    ax.set_xticks(range(len(motivos)))
    ax.set_xticklabels(motivos, rotation=45, ha='right')
    plt.tight_layout()

    # Convertir la gráfica a imagen base64
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', bbox_inches='tight')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')
    plt.close(fig)

    img_stream_excel = io.BytesIO()
    plt.savefig(img_stream_excel, format='png')
    img_stream_excel.seek(0)

    # Retornar la imagen como cadena base64
    return img_base64, img_stream_excel

#ELIMINAR REPORTE CALL-CENTER
def delete_report(request, zone):

    if request.method == 'POST':
        # Obtener la lista de reportes desde la sesión
        reports = request.session.get('reports', [])

        # Filtrar los reportes para eliminar el reporte con la zona especificada
        request.session['reports'] = [report for report in reports if report['zone'] != zone]

    return redirect('generate_report')

#LOGIA PARA REPORTE WHATICKET
def whaticket(request):
    form = ChatForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        zona = form.cleaned_data['zona']
        sucursal = form.cleaned_data['sucursal']
        nombre_personal = form.cleaned_data['nombre_personal']
        chats_creados = form.cleaned_data['chats_creados']
        chats_resueltos = form.cleaned_data['chats_resueltos']

        # Guardar los datos en la base de datos o realizar otra acción necesaria
        # Por ejemplo, guardarlos en un modelo específico para registros de chats

        # Redirigir o renderizar de nuevo la página
        return redirect('whaticket')  # Puedes redirigir a la misma página o a otra vista

    context = {
        'form': form,
    }
    return render(request, 'core/whaticket.html', context)

#INICIO REPORTE CAJERO
def reporte_cajero(request):
    reporte_caja = []
    total_internet_calls = 0
    pie_chart_caja = None
    category_calls_caja = {category: 0 for category in COUNT_CATEGORIES}  # Inicializamos aquí

    if request.method == 'POST':
        form = ReporteForm(request.POST, request.FILES)
        if form.is_valid():
            sucursal = form.cleaned_data['sucursal']
            archivo_excel = request.FILES.get('archivo_excel')

            if archivo_excel is None:
                return HttpResponse("No se ha proporcionado un archivo.", status=400)

            agentes = PersonalCaja.objects.all().values_list('nombre_usuario_perseo', flat=True)
            nombres_agentes = set(agentes)

            try:
                df = pd.read_excel(archivo_excel)

                nombres_en_excel = set(df['NOMBRE_AGENTE'])
                nombres_no_en_bd = nombres_en_excel - nombres_agentes
                if nombres_no_en_bd:
                    print(f"Nombres en el archivo Excel que no están en la base de datos: {nombres_no_en_bd}")

                df_filtrado = df[df['NOMBRE_AGENTE'].isin(nombres_agentes)]
                df_filtrado = df_filtrado[~df_filtrado['CATEGORIA_LLAMADA'].isin(EXCLUDE_CATEGORIES)]
                df_filtrado = df_filtrado[~df_filtrado['MOTIVO_LLAMADA'].isin(EXCLUDE_REASONS)]

                total_calls = df_filtrado.shape[0]
                agent_calls = {agente: df_filtrado[df_filtrado['NOMBRE_AGENTE'] == agente].shape[0] for agente in nombres_agentes}
                agent_calls = {agente: llamadas for agente, llamadas in agent_calls.items() if llamadas > 0}

                missing_keys = [agente for agente in nombres_agentes if agente not in agent_calls]
                if missing_keys:
                    print(f"Agentes en la base de datos que no tienen llamadas: {missing_keys}")

                category_calls_caja = {category: df_filtrado[df_filtrado['CATEGORIA_LLAMADA'] == category].shape[0] for category in COUNT_CATEGORIES}

                motivo_calls = {motivo: df_filtrado[(df_filtrado['CATEGORIA_LLAMADA'] == 'ACLARACIONES/CONSULTA') & (df_filtrado['MOTIVO_LLAMADA'] == motivo)].shape[0] for motivo in COUNT_MOTIVOS_ACLARACIONES}

                tv_filtered_df = df_filtrado[df_filtrado['CATEGORIA_LLAMADA'] == 'QUEJAS DE SERVICIO DE TV']
                tv_motivo_counts = {key: tv_filtered_df[tv_filtered_df['MOTIVO_LLAMADA'].isin(motivos)].shape[0] for key, motivos in COUNT_MOTIVOS_TV.items()}
                tv_motivo_counts['TOTAL'] = sum(tv_motivo_counts.values())

                internet_calls = {motivo: df_filtrado[(df_filtrado['CATEGORIA_LLAMADA'] == 'QUEJAS DE SERVICIO DE INTERNET') & (df_filtrado['MOTIVO_LLAMADA'] == motivo)].shape[0] for motivo in COUNT_MOTIVOS_INTERNET}
                total_internet_calls = sum(internet_calls.values())

                redes_sociales_calls = {motivo: df_filtrado[(df_filtrado['CATEGORIA_LLAMADA'] == 'REDES SOCIALES') & (df_filtrado['MOTIVO_LLAMADA'] == motivo)].shape[0] for motivo in COUNT_MOTIVOS_REDES}

                reporte_caja = request.session.get('reporte_caja', [])
                report_found = False

                for report in reporte_caja:
                    if report.get('zone') == sucursal:
                        report.update({
                            'agent_calls': agent_calls,
                            'category_calls': category_calls_caja,
                            'motivo_calls': motivo_calls,
                            'tv_motivo_calls': tv_motivo_counts,
                            'internet_calls': internet_calls,
                            'total_internet_calls': total_internet_calls,
                            'redes_sociales_calls': redes_sociales_calls,
                            'total_calls': total_calls,
                            'total_calls_aclaraciones': sum(motivo_calls.values())
                        })
                        report_found = True
                        break

                if not report_found:
                    reporte_caja.append({
                        'zone': sucursal,
                        'agent_calls': agent_calls,
                        'category_calls': category_calls_caja,
                        'motivo_calls': motivo_calls,
                        'tv_motivo_calls': tv_motivo_counts,
                        'internet_calls': internet_calls,
                        'redes_sociales_calls': redes_sociales_calls,
                        'total_internet_calls': total_internet_calls,
                        'total_calls': total_calls,
                        'total_calls_aclaraciones': sum(motivo_calls.values())
                    })

                request.session['reporte_caja'] = reporte_caja

                return redirect('reportecaja')

            except Exception as e:
                return HttpResponse(f"Error al procesar el archivo: {str(e)}", status=500)
        else:
            return HttpResponse("Formulario inválido.", status=400)

    else:
        form = ReporteForm()
        reporte_caja = request.session.get('reporte_caja', [])
        pie_chart_caja = request.session.get('pie_chart_caja', None)

        agentes = PersonalCaja.objects.all().values_list('nombre_usuario_perseo', flat=True)
        nombres_agentes = set(agentes)
        total_calls_by_agent_caja = {agente_caja: 0 for agente_caja in nombres_agentes}
        for report in reporte_caja:
            for agente_caja, llamadas in report.get('agent_calls', {}).items():
                total_calls_by_agent_caja[agente_caja] += llamadas

        total_calls_all_zones = sum(report.get('total_calls', 0) for report in reporte_caja)
    
        total_category_calls = {category: 0 for category in COUNT_CATEGORIES}

        # Llamar a la función de generación de gráficos aquí
        pie_chart_caja = generate_pie_chart_caja(reporte_caja)
        bar_chart_caja = generate_bar_chart_caja(reporte_caja)
        bar_chart_aclaraciones_caja = generate_aclaraciones_bar_chart_caja(reporte_caja)
        bar_chart_tv_caja = generate_tv_motivo_bar_chart_caja(reporte_caja)
        bar_chart_internet_caja = generate_internet_bar_chart_caja(reporte_caja)
        bar_chart_rs_caja = generate_redes_sociales_bar_chart(reporte_caja)

        request.session['pie_chart_caja'] = pie_chart_caja    
        request.session['bar_chart_caja'] = bar_chart_caja
        request.session['bar_chart_aclaraciones_caja'] = bar_chart_aclaraciones_caja
        request.session['bar_chart_tv_caja'] = bar_chart_tv_caja
        request.session['bar_chart_internet'] = bar_chart_internet_caja
        request.session['bar_chart_rs_caja'] = bar_chart_rs_caja
        

        
        for report in reporte_caja:
            for category, count in report.get('category_calls', {}).items():
                total_category_calls[category] += count

        category_chart_caja = generate_category_bar_chart_caja(total_category_calls)  # category_calls_caja ya está inicializado
        request.session['category_chart_caja'] = category_chart_caja

        total_internet_calls = sum(report.get('total_internet_calls', 0) for report in reporte_caja)
        print(f"Total de quejas de servicio de Internet: {total_internet_calls}")

        return render(request, 'core/reportecaja.html', {
            'form': form,
            'reporte_caja': reporte_caja,
            'total_calls_all_zones': total_calls_all_zones,
            'count_motivos_aclaraciones': COUNT_MOTIVOS_ACLARACIONES,
            'counts_motivos_tv': COUNT_MOTIVOS_TV.keys(),
            'count_motivos_internet': COUNT_MOTIVOS_INTERNET,
            'count_motivos_redes': COUNT_MOTIVOS_REDES,
            'total_category_calls': total_category_calls,
            'total_internet_calls': total_internet_calls,
            'pie_chart_caja': pie_chart_caja,
            'bar_chart_caja': bar_chart_caja,
            'category_chart_caja': category_chart_caja,
            'bar_chart_aclaraciones_caja': bar_chart_aclaraciones_caja,
            'bar_chart_tv_caja': bar_chart_tv_caja,
            'bar_chart_internet_caja': bar_chart_internet_caja,
            'bar_chart_rs_caja': bar_chart_rs_caja
        })

#GRAFICAS DE REPORTE CAJA    
def generate_pie_chart_caja(reporte_caja):
    try:
        zones = [report['zone'] for report in reporte_caja]  # 'zone' en lugar de 'sucursal'
        total_calls = [report['total_calls'] for report in reporte_caja]

        if not zones or not total_calls:
            raise ValueError("Los datos de llamadas o zonas están vacíos.")
        
        # Depuración
        print(f"Zonas: {zones}")
        print(f"Total de llamadas: {total_calls}")

        fig, ax = plt.subplots(figsize=(10, 6))
        wedges, texts, autotexts = ax.pie(total_calls, labels=zones, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired(range(len(zones))))
        ax.set_title('Total de Llamadas por Zona', fontsize=16, weight='bold')

        for text in texts:
            text.set_fontsize(9)
            text.set_color('black')

        for autotext in autotexts:
            autotext.set_fontsize(8)
            autotext.set_color('black')

        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        graphic = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()

        return graphic
    except Exception as e:
        print(f"Error al generar el gráfico: {str(e)}")
        return None

def generate_bar_chart_caja(reporte_caja):
    # Obtener los agentes y sus llamadas totales en todos los reportes
    agentes = PersonalCaja.objects.all().values_list('nombre_usuario_perseo', flat=True)
    nombres_agentes = set(agentes)
    total_calls_by_agent_caja = {agente_caja: 0 for agente_caja in nombres_agentes}
    for report in reporte_caja:
        for agente, llamadas in report['agent_calls'].items():
            total_calls_by_agent_caja[agente] += llamadas

    # Crear la figura de Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(total_calls_by_agent_caja.keys(), total_calls_by_agent_caja.values())
    ax.set_xlabel('Agentes')
    ax.set_ylabel('Número de Llamadas')
    ax.set_title('Número de Llamadas por Agente en Todas las Zonas')

    # Rotar las etiquetas del eje x para mejor legibilidad si hay muchas
    plt.xticks(rotation=45, ha='right')

    # Ajustar la disposición para que se vea mejor
    plt.tight_layout()

    # Guardar la figura en un buffer de BytesIO
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)  # Volver al inicio del buffer

    # Convertir el buffer en una cadena base64 para incrustar en HTML
    graphic = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Cerrar la figura para liberar recursos
    plt.close(fig)

    return graphic

def generate_category_bar_chart_caja( total_category_calls):
    # Filtrar la categoría 'TOTAL DE LLAMADA'
    filtered_category_calls = {category: count for category, count in  total_category_calls.items() if category != 'TOTAL DE LLAMADA'}
    
    # Verificar si las categorías y los valores son correctos
    print(f"Categorías: {list(filtered_category_calls.keys())}")
    print(f"Llamadas: {list(filtered_category_calls.values())}")
    
    # Establecer el tamaño de la figura
    fig, ax = plt.subplots(figsize=(10, 6))
    categories = list(filtered_category_calls.keys())
    calls = list(filtered_category_calls.values())

    # Si los valores son todos cero o negativos, la gráfica aparecerá vacía
    if all(call == 0 for call in calls):
        print("Todos los valores son cero, no se mostrará la gráfica.")
    
    # Crear la gráfica de barras
    ax.bar(categories, calls)
    ax.set_xlabel('Categorías')
    ax.set_ylabel('Número de Llamadas')
    ax.set_title('Número de Llamadas por Categoría')
    plt.xticks(rotation=45, ha='right')

    
    # Ajustar los márgenes
    plt.tight_layout()

    # Guardar la imagen en el buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close(fig)
    return graphic

def generate_aclaraciones_bar_chart_caja(reporte_caja):
    # Obtener los nombres de los motivos de aclaraciones/consulta
    motivos = [
        'ESTATUS DE ORDEN DE SERVICIO',
        'INFORMACION DE SUCURSALES',
        'INFORMACION DE SALDO',
        'BARRA DE CANALES',
        'INFORMACION DE PROMOCIONES / PAQUETES',
        'PAGINA WEB / REDES SOCIALES',
        'OTROS',
        'LLAMADA AVISO DE CORTE'
    ]

    # Inicializar listas para contar las llamadas por motivo
    llamadas_por_motivo = {motivo: 0 for motivo in motivos}

    # Sumar las llamadas por motivo en todos los reportes
    for report in reporte_caja:
        motivo_calls = report.get('motivo_calls', {})
        for motivo, count in motivo_calls.items():
            if motivo in llamadas_por_motivo:
                llamadas_por_motivo[motivo] += count

    # Convertir los datos a listas para el gráfico de barras
    motivos = list(llamadas_por_motivo.keys())
    counts = list(llamadas_por_motivo.values())

    # Configurar el gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(motivos))
    width = 0.5
    plt.subplots_adjust(bottom=0.4)  # Aumentar el margen inferior

    bars = ax.bar(x, counts, width, label='Llamadas por motivo', color='green')

    ax.set_xlabel('Motivos de Aclaraciones/Consulta')
    ax.set_ylabel('Cantidad de Llamadas')
    ax.set_title('Llamadas por Motivo en Aclaraciones/Consulta')
    ax.set_xticks(x)
    ax.set_xticklabels(motivos, rotation=45, ha='right', fontsize=10)  # Ajustar el tamaño de fuente
    ax.legend()

    # Añadir etiquetas con los valores en cada barra
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

    # Convertir el gráfico a imagen PNG en memoria
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Convertir la imagen a base64 para incrustarla en la plantilla HTML
    graphic = base64.b64encode(image_png).decode('utf-8')
    plt.close(fig)
    return graphic

def generate_tv_motivo_bar_chart_caja(reporte_caja):
    # Inicializar diccionario para contar las llamadas por motivo de TV
    tv_motivo_counts = {key: 0 for key in COUNT_MOTIVOS_TV.keys()}

    # Sumar las llamadas por motivo en todos los reportes
    for report in reporte_caja:
        tv_motivo_calls = report.get('tv_motivo_calls', {})
        for motivo, count in tv_motivo_calls.items():
            if motivo in tv_motivo_counts:
                tv_motivo_counts[motivo] += count

    # Convertir los datos a listas para el gráfico de barras
    motivos = list(tv_motivo_counts.keys())
    counts = list(tv_motivo_counts.values())

    # Configurar el gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(motivos))
    width = 0.5
    plt.subplots_adjust(bottom=0.5)

    bars = ax.bar(x, counts, width, label='Llamadas por motivo', color='green')

    ax.set_xlabel('Motivos de Quejas de TV')
    ax.set_ylabel('Cantidad de Llamadas')
    ax.set_title('Llamadas por Motivo en Quejas de Servicio de TV')
    ax.set_xticks(x)
    ax.set_xticklabels(motivos, rotation=45, ha='right')
    ax.legend()

    # Añadir etiquetas con los valores en cada barra
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

    # Convertir el gráfico a imagen PNG en memoria
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Convertir la imagen a base64 para incrustarla en la plantilla HTML
    graphic = base64.b64encode(image_png).decode('utf-8')
    plt.close(fig)
    return graphic

def generate_internet_bar_chart_caja(reporte_caja):
    motivos = list(COUNT_MOTIVOS_INTERNET)
    llamadas_por_motivo = {motivo: 0 for motivo in motivos}

    for report in reporte_caja:
        internet_calls = report.get('internet_calls', {})
        for motivo, count in internet_calls.items():
            if motivo in llamadas_por_motivo:
                llamadas_por_motivo[motivo] += count

    motivos = list(llamadas_por_motivo.keys())
    counts = list(llamadas_por_motivo.values())

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(motivos))  # Ajuste para centrar el gráfico
    width = 0.5
    plt.subplots_adjust(bottom=0.4)

    bars = ax.bar(x, counts, width, label='Llamadas por motivo', color='green')

    ax.set_xlabel('Motivos de Quejas de Internet')
    ax.set_ylabel('Cantidad de Llamadas')
    ax.set_title('Llamadas por Motivo en Quejas de Internet')
    ax.set_xticks(x)
    ax.set_xticklabels(motivos, rotation=45, ha='right')
    ax.legend()

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png).decode('utf-8')
    plt.close(fig)
    return graphic

def generate_redes_sociales_bar_chart(reporte_caja):
    motivos = list(COUNT_MOTIVOS_REDES)
    llamadas_por_motivo = {motivo: 0 for motivo in motivos}

    for report in reporte_caja:
        redes_sociales_calls = report.get('redes_sociales_calls', {})
        for motivo, count in redes_sociales_calls.items():
            if motivo in llamadas_por_motivo:
                llamadas_por_motivo[motivo] += count

    motivos = list(llamadas_por_motivo.keys())
    counts = list(llamadas_por_motivo.values())

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(motivos))
    width = 0.5
    plt.subplots_adjust(bottom=0.4)

    bars = ax.bar(x, counts, width, label='Llamadas por motivo', color='green')

    ax.set_xlabel('Motivos de Quejas en Redes Sociales')
    ax.set_ylabel('Cantidad de Llamadas')
    ax.set_title('Llamadas por Motivo en Quejas de Redes Sociales')
    ax.set_xticks(x)
    ax.set_xticklabels(motivos, rotation=45, ha='right')
    ax.legend()

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png).decode('utf-8')
    plt.close(fig)
    return graphic

#ELIMINAR REPORTE CAJA
def delete_report_caja(request, zone):
    if request.method == 'POST':
        # Obtener la lista de reportes desde la sesión
        reporte_caja = request.session.get('reporte_caja', [])
        # Filtrar los reportes para eliminar el reporte con la zona especificada
        request.session['reporte_caja'] = [report for report in reporte_caja if report['zone'] != zone]
    return redirect('reportecaja')
