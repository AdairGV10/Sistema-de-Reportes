from django import forms
from .models import Personal
from .models import PersonalCaja

class PersonalForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = '__all__'  # Esto ahora incluirá el nuevo campo

class ChatForm(forms.Form):

    zona_choices = [
        ('Xaltianguis', 'Zona Xaltianguis'),
        ('Tlaxcoapan', 'Zona Tlaxcoapan'),
        ('Tula', 'Zona Tula de Allende'),
    ]

    zona = forms.ChoiceField(choices=zona_choices, label='Zona')
    sucursal = forms.ChoiceField(choices=[], label='Sucursal', required=False)
    chats_creados = forms.IntegerField(label='Chats Creados')
    chats_resueltos = forms.IntegerField(label='Chats Resueltos')
    nombre_personal = forms.ChoiceField(choices=[], label='Nombre del Personal')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sucursal'].choices = []
        self.fields['nombre_personal'].choices = []

        # Definir las opciones de sucursal basadas en la zona seleccionada
        self.fields['sucursal'].choices = []

        if 'zona' in self.data:
            try:
                zona_seleccionada = self.data.get('zona')
                if zona_seleccionada == 'Xaltianguis':
                    sucursales_xaltianguis = [
                        ('JACALA', 'JACALA'),
                        ('SAN AGUSTIN TLAXIACA', 'SAN AGUSTIN TLAXIACA'),
                        ('SAN JOSE TEPENENE', 'SAN JOSE TEPENENE'),
                        ('ACTOPAN', 'ACTOPAN'),
                        ('PROGRESO', 'PROGRESO'),
                        ('MIXQUIAHUALA', 'MIXQUIAHUALA'),
                        ('TLAHUELILPAN', 'TLAHUELILPAN'),
                        ('APSXCO AZUL', 'APSXCO AZUL'),
                        ('TEQUIXQUIAC', 'TEQUIXQUIAC'),
                    ]
                    self.fields['sucursal'].choices = sucursales_xaltianguis
                elif zona_seleccionada == 'Tlaxcoapan':
                    sucursales_tlaxcoapan = [
                        ('Tlaxcoapan', 'Tlaxcoapan'),
                        ('Atitalaquia', 'Atitalaquia'),
                    ]
                    self.fields['sucursal'].choices = sucursales_tlaxcoapan
                elif zona_seleccionada == 'Tula':
                    sucursales_tula = [
                        ('Tezontepec', 'Tezontepec'),
                        ('Rula de allende', 'Rula de allende'),
                        ('Apaxco teleimagen', 'Apaxco teleimagen'),
                    ]
                    self.fields['sucursal'].choices = sucursales_tula

                # Obtener nombres de personal para el campo de selección
                personal_names = Personal.objects.values_list('name', flat=True)
                choices = [(name, name) for name in personal_names]
                self.fields['nombre_personal'].choices = choices

            except (TypeError, ValueError):
                pass  # Manejar errores si es necesario

class PersonalCajaForm(forms.ModelForm):
    class Meta:
        model = PersonalCaja
        fields = ['nombre_completo', 'sucursal', 'nombre_usuario_perseo']
        widgets = {
            'sucursal': forms.Select(choices=PersonalCaja.SUCURSALES_CHOICES),
        }

SUCURSALES_CHOICES = [
    ('JACALA', 'JACALA'),
    ('SAN AGUSTIN TLAXIACA', 'SAN AGUSTIN TLAXIACA'),
    ('ACTOPAN CIMA', 'ACTOPAN CIMA'),
    ('ACTOPAN OCAMPO', 'ACTOPAN OCAMPO'),
    ('SAN JOSE TEPENENE', 'SAN JOSE TEPENENE'),
    ('ACTOPAN TUZO', 'ACTOPAN TUZO'),
    ('PROGRESO DE OBREGON', 'PROGRESO DE OBREGON'),
    ('MIXQUIAHUALA', 'MIXQUIAHUALA'),
    ('TUZO MIXQUIAHUALA', 'TUZO MIXQUIAHUALA'),
    ('TLAHUELILPAN', 'TLAHUELILPAN'),
    ('APAXCO TELECABLE', 'APAXCO TELECABLE'),
    ('TEQUIXQUIAC', 'TEQUIXQUIAC'),
    ('ACAXOCHITLAN', 'ACAXOCHITLAN'),
    ('TENANGO', 'TENANGO'),
    ('EL CEREZO', 'EL CEREZO'),
]

class ReporteForm(forms.Form):
    sucursal = forms.ChoiceField(choices=SUCURSALES_CHOICES, label='Zona', widget=forms.Select(attrs={'class': 'form-control'}))
    archivo_excel = forms.FileField(label='Cargar archivo Excel', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))


class ZoneSelectionForm(forms.Form):
    zone = forms.ChoiceField(choices=[
        ('ZONA XALTIANGUIS', 'ZONA XALTIANGUIS'),
        ('ZONA TLAXCOAPAN', 'ZONA TLAXCOAPAN'), 
        ('ZONA TULA DE ALLENDE', 'ZONA TULA DE ALLENDE'), 
    ], label='Zona')

class BranchSelectionForm(forms.Form):
    branch = forms.ChoiceField(choices=[], label='Sucursal', required=False)
    file = forms.FileField(label='Cargar archivo Excel', required=False)  # Añadir fuera del bloque condicional

    def __init__(self, *args, **kwargs):
        zone = kwargs.pop('zone', None)  # Obtener la zona seleccionada
        super().__init__(*args, **kwargs)

        # Establecer las sucursales en función de la zona seleccionada
        if zone == 'ZONA XALTIANGUIS':
            self.fields['branch'].choices = [
                ('Xaltianguis', 'Xaltianguis'),
                # ... otras sucursales
            ]
        elif zone == 'ZONA TLAXCOAPAN':
            self.fields['branch'].choices = [
                ('Tlaxcoapan', 'Tlaxcoapan'),
                ('Atitalaquia', 'Atitalaquia'),
            ]
        elif zone == 'ZONA TULA DE ALLENDE':
            self.fields['branch'].choices = [
                ('Tula de Allende', 'Tula de Allende'),
                ('Tezontepec de Aldama', 'Tezontepec de Aldama'),
                ('Apaxco Teleimagen', 'Apaxco Teleimagen'),
            ]